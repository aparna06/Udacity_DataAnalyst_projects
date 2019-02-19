###update XML

#import modules
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

#import modules that were created for auditing
import audit_phone
import audit_street_names
import audit_zipcode

osmfile="map.osm"

#function to update XML
def update_xml(osmfile):
    osm_file = open(osmfile, "r")
    tree=ET.parse(osm_file)
    root=tree.getroot()
    for elem in root:
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if audit_phone.is_phone(tag):
                    tag.attrib['v']=audit_phone.newphone[tag.attrib['v']]
                if audit_street_names.is_street_name(tag):
                    if tag.attrib['v'] in audit_street_names.newname.keys():
                        tag.attrib['v']=audit_street_names.newname[tag.attrib['v']]
                        #print("-->",tag.attrib['v'])
                if audit_zipcode.is_zipcode(tag):
                    if tag.attrib['v'] in audit_zipcode.newcode.keys():
                        tag.attrib['v']= audit_zipcode.newcode[tag.attrib['v']]
    return(tree)
                    
tree=update_xml(osmfile)

tree.write("output.osm")
