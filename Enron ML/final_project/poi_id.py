#!/usr/bin/python

import sys
import pickle
import pandas as pd
sys.path.append("../tools/")


from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif

from sklearn.model_selection import GridSearchCV
from sklearn import svm, tree
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import classification_report
from sklearn.metrics import f1_score, recall_score, make_scorer

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

enronDf=pd.DataFrame(data_dict).transpose()

### Task 1: Select what features you'll use.
features_list = ['poi',
                 'salary',
                 'bonus',
                 'expenses',
                 'total_payments',
                 'total_stock_value',
                 'exercised_stock_options',
                 'long_term_incentive',
                 'deferral_payments',
                 'deferred_income',
                 'restricted_stock',
                 'restricted_stock_deferred',
                 'from_messages',
                 'from_poi_to_this_person',
                 'from_this_person_to_poi',
                 'shared_receipt_with_poi',
                 'to_messages'                 
                 ]


### Task 2: Remove outliers & cleaning up data
def fillNaNAsZero(x):
    if x == "NaN":
        return 0
    else:
        return x

print("Summary statistics of columns of interest:")   
print(enronDf[features_list].describe())


enronDf.to_csv("ENRON.txt",sep="\t")

enronDf.loc['BHATNAGAR SANJAY','total_payments'] = 137864
enronDf.loc['BHATNAGAR SANJAY','expenses'] = 137864
enronDf.loc['BHATNAGAR SANJAY','other'] = 0
enronDf.loc['BHATNAGAR SANJAY','director_fees'] = 0
enronDf.loc['BHATNAGAR SANJAY','exercised_stock_options'] = 15456290
enronDf.loc['BHATNAGAR SANJAY','restricted_stock'] = 2604490
enronDf.loc['BHATNAGAR SANJAY','restricted_stock_deferred'] = -2604490
enronDf.loc['BHATNAGAR SANJAY','total_stock_value'] = 15456290

enronDf.loc['BELFER ROBERT','deferred_income'] = -102500
enronDf.loc['BELFER ROBERT','deferral_payments'] = 0
enronDf.loc['BELFER ROBERT','expenses'] = 3285
enronDf.loc['BELFER ROBERT','director_fees'] = 102500
enronDf.loc['BELFER ROBERT','total_payments'] = 3285
enronDf.loc['BELFER ROBERT','exercised_stock_options'] = 0
enronDf.loc['BELFER ROBERT','restricted_stock'] = 44093
enronDf.loc['BELFER ROBERT','restricted_stock_deferred'] = -44093
enronDf.loc['BELFER ROBERT','total_stock_value'] = 0

for col in features_list[1:]:
    enronDf[col]=enronDf[col].apply(fillNaNAsZero)
    enronDf[col]=pd.to_numeric(enronDf[col])
    

def find_Missing(row):
    tooManyMissing=False;
    count=0
    for x in row:
        if not isinstance(x,bool) and (x == 0 or x == 'NaN') :
            count+=1;
    if float(count)/len(row) >= 0.85:
        tooManyMissing =True;       
    return(tooManyMissing)

removeNames=[]
for i,row in enronDf.iterrows():
    if find_Missing(row):
        removeNames.append(row.name)

print "Removing", len(removeNames), "individuals who had greater than or equal to 15% missing data."
enronDf.drop(removeNames,inplace=True)
print "Individuals removed", str(removeNames)

maxID=enronDf[features_list[1:]].idxmax(axis=0)

print("Name of row with 'maximum' in each column:")
print(maxID)

enronDf.drop("TOTAL",axis=0,inplace=True)


maxID=enronDf[features_list[1:]].idxmax(axis=0)
print("\n")
print("Name of row with 'maximum' after removal of row indexed as 'TOTAL' in each column:")
print(maxID)

print("\nNumber of POI and non-POI individuals:")
print(enronDf.poi.value_counts())

def plot_graph(data,xlab="", ylab=""):
    import matplotlib.pyplot
    from matplotlib.patches import Patch

    color=["red","blue"]
    legend_elements=[Patch(color="red",label="POI"),
                     Patch(color="blue",label="non-POI")]
    
    for i,point in data.iterrows():
        x = point[0]
        y = point[1]
        poi=point[2]
        matplotlib.pyplot.scatter(x,y,c=color[int(poi)],alpha=0.5)

    matplotlib.pyplot.xlabel(xlab)
    matplotlib.pyplot.ylabel(ylab)
    matplotlib.pyplot.title(xlab+" vs "+ylab)
    matplotlib.pyplot.legend(handles=legend_elements)
    matplotlib.pyplot.show()

    pass

#plot_graph(enronDf[["salary","bonus","poi"]],xlab="salary",ylab="bonus")
#plot_graph(enronDf[["from_poi_to_this_person","from_this_person_to_poi","poi"]],xlab="from POI", ylab="to POI")

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = enronDf.to_dict('index')

def compute_proportion(poimsg,allmsg):
    proportion=0
    if float(poimsg)!=0 and float(allmsg)!=0:
        proportion=float(poimsg)/float(allmsg)
    return proportion

for name in my_dataset:
    data_point = my_dataset[name]

    frompoi= data_point["from_poi_to_this_person"]
    tomsg = data_point["to_messages"]
    propFromPoi = compute_proportion( frompoi, tomsg )

    sharedpoi=data_point["shared_receipt_with_poi"]
    propSharePoi = compute_proportion(sharedpoi,tomsg)
    
    data_point["propFromPoi"] = propFromPoi
    data_point["propSharePoi"]= propSharePoi
    
    topoi = data_point["from_this_person_to_poi"]
    frommsg = data_point["from_messages"]
    propToPoi = compute_proportion(topoi, frommsg)

    data_point["propToPoi"] = propToPoi
    
    my_dataset[name]=data_point

features_list.extend(['propFromPoi',
                 'propToPoi',
                 'propSharePoi'])

#my_datasetDf=pd.DataFrame(my_dataset).transpose()
#plot_graph(my_datasetDf[['propFromPoi','propToPoi','poi']],xlab="Proportion from POI", ylab="Proportion to POI")

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

sss=StratifiedShuffleSplit(n_splits=100, test_size=0.3, random_state=42)
sss.get_n_splits(features, labels)       
 
for train_index,test_index in sss.split(features, labels):
   #print("TRAIN:", train_index, "TEST:", test_index)
   features_train=[]
   features_test =[]

   labels_train=[]
   labels_test=[]

   for i in train_index:
       features_train.append(features[i])
       labels_train.append(labels[i])
   for j in test_index:
       features_test.append(features[j])
       labels_test.append(labels[j])


my_scorer = make_scorer(recall_score, pos_label=1, average="binary")
feature_transforms=FeatureUnion([('scaling',preprocessing.RobustScaler()),
                                 ('kbest', SelectKBest(f_classif)),
                                 #('pca', PCA())
                               ])

pipe=Pipeline([
    ('feature_transforms',feature_transforms),

    #SVM
    #('clf',svm.SVC(kernel='rbf'))

    #Decision Tree
    #('clf', tree.DecisionTreeClassifier(random_state=42))

    #RandomForestClassifier
    #('clf', RandomForestClassifier(max_features=None))

    #KNeighbors Classifier
    #('clf',KNeighborsClassifier())

    #ExtraTreeClassifier
    #('clf', ExtraTreesClassifier(max_features=None, bootstrap=False))

    #AdaBoostClassifier
    ('clf', AdaBoostClassifier())
    ])

gridSearch=GridSearchCV(pipe, {
    'feature_transforms__kbest__k': [2, 3, 5, 10,16],
    #'feature_transforms__pca__n_components':[1,2,3],
    
    #SVM
    #'clf__C': [1, 5, 10, 20, 200, 1000],
    #'clf__class_weight' :[None, 'balanced'],
    #'clf__gamma':[1,0.01]

    #Decision Tree
    #'clf__criterion':['gini','entropy'],
    #'clf__min_samples_split':[2,3,5,10],

    #Random Forest Classifier
    #'clf__criterion':['gini','entropy'],
    #'clf__min_samples_split':[2,3,5,10,20],
    #'clf__n_estimators':[3,5,10,20,50],
    #'clf__min_samples_leaf':[1,2,5],

    #KNeighbors Classifier
    #'clf__n_neighbors':[2,3,5,10],
    #'clf__algorithm':["ball_tree", "kd_tree", "brute"],
    #'clf__leaf_size':[3,5,10,100]

    #Extra Tree Classifer
    #'clf__criterion':['gini','entropy'],
    #'clf__min_samples_split':[2,3,5,10,20],
    #'clf__n_estimators':[3,5,10,20,50],
    #'clf__min_samples_leaf':[1,2,5]

    #AdaBoostClassifier
    'clf__n_estimators':[3,5,10,20,50],
    
    }, iid=True, cv=5, scoring= my_scorer)

gridSearch.fit(features_train, labels_train)

clf=pipe.set_params(**gridSearch.best_params_)
pipe.fit(features_train,labels_train)

print("Best Parameters after grid search:")
print(gridSearch.best_params_)
print("\n")

pred=clf.predict(features_test)
res=classification_report(labels_test, pred)
print("Classification report:")
print(res)


### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)   
#

#printing Scores of the features
k=gridSearch.get_params(True)['estimator__feature_transforms__transformer_list'][1][1]
features_scores = zip(features_list[1:], k.scores_)
for feature, score in sorted(features_scores, key=lambda x:x[1], reverse=True):
    print('%s : %s' % (feature, score))
    
