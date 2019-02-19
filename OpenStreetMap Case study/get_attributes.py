#import modules
import xml.etree.cElementTree as ET
import pandas as pd

##function to populate node attributes in to dictionary
def get_node_attributes(node):   
    return {"id": int(node.attrib["id"]),
            "user":node.attrib["user"],
            "uid":int(node.attrib["uid"]),
            "version":int(node.attrib["version"]),
            "lat":float(node.attrib["lat"]),
            "lon":float(node.attrib["lon"]),
            "timestamp":node.attrib["timestamp"],
            "changeset":int(node.attrib["changeset"])}

##function to populate node or way tag attributes in to dictionary
def get_tag_attributes(elem):
    tag_dicts=[]
    for tag in elem.iter("tag"):
        #print(tag.attrib);
        tag_dict={}
        tag_dict["id"]=int(elem.attrib["id"])
        tmp=tag.attrib["k"].split(":")
        if ":" in tag.attrib["k"]:
            tag_dict["key"]=""
            for i in tmp[1:]:
                tag_dict["key"]+=i
                tag_dict["key"]+=":"
            tag_dict["key"]=tag_dict["key"][0:(len(tag_dict["key"])-1)]
            tag_dict["value"]=tag.attrib["v"]
            tag_dict["type"]=tmp[0]
        else:
            tag_dict["key"]=tag.attrib["k"]
            tag_dict["value"]=tag.attrib["v"]
            tag_dict["type"]="regular"
        tag_dicts.append(tag_dict)
    return(tag_dicts)

##function to populate way attributes in to dictionary
def get_way_attributes(way):
    return {"id":int(way.attrib["id"]),
            "user":way.attrib["user"],
            "uid":int(way.attrib["uid"]),
            "version":int(way.attrib["version"]),
            "timestamp":way.attrib["timestamp"],
            "changeset":int(way.attrib["changeset"])}

#function to populate way node attributes in to dictionary
def get_way_nodes(elem):
    way_nodes=[]
    for pos,nd in enumerate(elem.iter("nd")):
        way_node_dict={"id":int(elem.attrib["id"]),
                       "node_id":int(nd.attrib["ref"]),
                       "position":int(pos)}
        way_nodes.append(way_node_dict)
    return way_nodes;
        

#assigning  the updated OSMFILE 
OSMFILE = "output.osm"

osm_file= open(OSMFILE, "r")

nodes=[]
node_tags=[]
ways=[]
way_tags=[]
way_nodes=[]
for event, elem in ET.iterparse(osm_file, events=("start",)):
    if elem.tag == "node":
        nodes.append(get_node_attributes(elem))
        tmp=get_tag_attributes(elem)
        if tmp:
            node_tags.extend(tmp)
    if elem.tag == "way":
        tmp=get_way_nodes(elem)
        if tmp:
            way_nodes.extend(tmp)
        ways.append(get_way_attributes(elem))
        tmp=get_tag_attributes(elem)
        if tmp:
            way_tags.extend(tmp)
            

## Dataframes of the dictionaries and ordering them
nodes_df=pd.DataFrame(nodes)
nodes_df=nodes_df[["id","user","uid","version","lat","lon","timestamp","changeset"]]
node_tags_df=pd.DataFrame(node_tags)
node_tags_df=node_tags_df[["id","key","value","type"]]
ways_df=pd.DataFrame(ways)
ways_df=ways_df[["id","user","uid","version","timestamp","changeset"]]
ways_tags_df=pd.DataFrame(way_tags)
ways_tags_df=ways_tags_df[["id","key","value","type"]]
ways_nodes_df=pd.DataFrame(way_nodes)
ways_nodes_df=ways_nodes_df[["id","node_id","position"]]

## check the length of dictionaries
print(nodes_df.shape, len(nodes))
print(node_tags_df.shape, len(node_tags))
print(ways_df.shape, len(ways))
print(ways_tags_df.shape, len(way_tags))
print(ways_nodes_df.shape, len(way_nodes))


## write out the data to csv files
nodes_df.to_csv("MyMapNodes.csv",encoding='utf-8',index=False,index_label=False)
node_tags_df.to_csv("MyMapNodeTags.csv",encoding='utf-8',index=False,index_label=False)
ways_df.to_csv("MyMapWays.csv",encoding='utf-8',index=False)
ways_tags_df.to_csv("MyMapWaysTags.csv",encoding='utf-8',index=False)
ways_nodes_df.to_csv("MyMapWaysNodes.csv",encoding='utf-8',index=False)

