## Auditing Street names

#import modules
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

#assigning OSMFILE 
OSMFILE = "map.osm"

#Regular expression for street type
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons","Circle", "Way", "Highway", "Northeast","Southeast",
            "South","Southwest","West","East"]

# Mapping dictionary to update abbreviated street names
mapping = { "St":"Street",
           "SE":"Southeast",
           "NE":"Northeast",
           "E":"East",
           "Hwy":"Highway",
            "Dr":"Drive",
           "DR": "Drive",
           "Dr.": "Drive",
           "Pl":"Place",
           "Ave":"Avenue"
            }

#function that audits street types
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
    return street_types

#function that checks if element attribute is street name
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

#function that audits the osmfile
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

#function that updates the name
def update_name(name, mapping):
    namearray=name.split(" ")
    newname=[]
    for element in namearray:
        for key in mapping.keys():
            if key == element:
                element=element.replace(key, mapping[key])
        newname.append(element) 

    return " ".join(newname)

#st_types contains a dictionary where street types are not as expected
st_types = audit(OSMFILE)
#pprint.pprint(dict(st_types))
#pprint.pprint("")

#for each street type in the dictionary, update the names and print them
newname=defaultdict(set)
for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            newname[name]=better_name
            #print(name, "=>", better_name)
#pprint.pprint(dict(newname))



