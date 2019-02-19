## Auditing Zipcode

#import modules
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

#assigning OSMFILE 
OSMFILE = "map.osm"


#function that checks if element attribute is postcode
def is_zipcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

#function that audits the osmfile
def audit(osmfile):
    osm_file = open(osmfile, "r")
    zipcodes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zipcode(tag) and len(tag.attrib['v'])>5:
                    zipcodes.add(tag.attrib['v'])
                        
    osm_file.close()
    return zipcodes

#function that normalizes the zipcode
def update_zipcode(zipcode):
        return(zipcode[0:5])

#zipcodes contains a set where zipcodes are not as expected
zipcodes = audit(OSMFILE)
#pprint.pprint(zipcodes)
#pprint.pprint("")

#for each zipcode in the set, update the names and print them
newcode=defaultdict(set)
for zipcode in zipcodes:
    better_zip = update_zipcode(zipcode)
    newcode[zipcode]=better_zip

#pprint.pprint(dict(newcode))



