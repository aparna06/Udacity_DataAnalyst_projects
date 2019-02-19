## Auditing Phone

#import modules
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

#assigning OSMFILE 
OSMFILE = "map.osm"

#function that checks if element attribute is phone
def is_phone(elem):
    return (elem.attrib['k'] == "phone")

#function that audits the osmfile
def audit(osmfile):
    osm_file = open(osmfile, "r")
    phones=set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_phone(tag):
                    phones.add(tag.attrib['v'])
                        
    osm_file.close()
    return phones

def update_phone(phone):
    phonetmp=phone.replace(" ","")
    phone=phonetmp.replace("(","")
    phonetmp=phone.replace(")","")
    phone=phonetmp.replace("-","")

    if len(phone)==10:
        phone="+1"+phone
    elif len(phone)==11:
        if phone.startswith("+"):
            phone=phone.replace("+","+1")
        else:
            phone="+"+phone

    newphone=""
    for i,char in enumerate(phone):       
        if i==2 or i==5 or i==8:
            newphone=newphone+"-"
            newphone+=char
        else:
            newphone=newphone+char
            
    return(newphone)
        
phones=audit(OSMFILE)


newphone=defaultdict(set)
for phone in phones:
    better_phone=update_phone(phone)
    newphone[phone]=better_phone

#pprint.pprint(dict(newphone))

    
