from xml.dom import minidom
from pathlib import Path
import csv

parent_path = Path(__file__).resolve().parent
parent_path = str(parent_path).replace("\\", "/")
input_path =  parent_path + "/" + "sample_text_node.xml"
tree = minidom.parse(input_path)

elems = tree.getElementsByTagName("country")

#make header
header = []
for elem in elems:
    if elem.nodeName not in header and elem.nodeName != "country":
        header.append(elem.nodeName)
    for node in list(elem.childNodes):
        #skip blank text node
        if(node.nodeType == node.TEXT_NODE):
            pass
        else:
            if node.nodeName not in header:
                header.append(node.nodeName)

output_path = parent_path + "/" + "output.csv"
f = open(output_path, "w", newline="")
writer = csv.writer(f)
writer.writerow(header)

#make data
for elem in elems:
    text = []
    text.append(elem.getElementsByTagName("rank")[0].childNodes[0].nodeValue)
    text.append(elem.getElementsByTagName("year")[0].childNodes[0].nodeValue)

    writer.writerow(text)

f.close()

            
tree.unlink()