from xml.dom import minidom
from pathlib import Path
import csv

parent_path = Path(__file__).resolve().parent
parent_path = str(parent_path).replace("\\", "/")
input_path =  parent_path + "/" + "sample.xml"
tree = minidom.parse(input_path)

elems = tree.getElementsByTagName("country")
print(elems[0].childNodes)
header = []
for elem in elems:
    if elem.nodeName not in header:
        header.append(elem.nodeName)
    for node in list(elem.childNodes):
        if(node.nodeType == node.TEXT_NODE):
            pass
        else:
            #for debug
            print(node)
            if node.nodeName not in header:
                header.append(node.nodeName)

output_path = parent_path + "/" + "output.csv"
with open(output_path, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
            
tree.unlink()