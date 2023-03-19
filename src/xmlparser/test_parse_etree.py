import xml.etree.ElementTree as ET
from pathlib import Path

parent_path = Path(__file__).resolve().parent
tree = ET.parse(parent_path.joinpath("sample.xml"))
root = tree.getroot()

for child1 in root:
    print(child1.tag, child1.attrib)
    for child2 in child1:
        #print(child2.tag, child2.attrib)
        print(child2.tag)
        print(child2.attrib)
'''
for neighbor in root.iter("Singapore"):
    print(neighbor.attrib)
'''