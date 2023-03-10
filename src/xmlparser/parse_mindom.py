from xml.dom import minidom
from pathlib import Path
import csv

parent_path = Path(__file__).resolve().parent
parent_path = str(parent_path).replace("\\", "/")
input_path =  parent_path + "/" + "sample.xml"
tree = minidom.parse(input_path)

output_path = parent_path + "/" + "output.csv"
f = open(output_path, "w")
writer = csv.writer(f)
writer.writerow("hello")

elems = tree.getElementsByTagName("country")
for elem in elems:
    for node in list(elem.childNodes):
        if(node.nodeType == node.TEXT_NODE):
            pass
        else:
            print(node)
            
tree.unlink()
f.close()