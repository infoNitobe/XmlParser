import xml.etree.ElementTree as ET
from pathlib import Path

parent_path = Path(__file__).resolve().parent
tree = ET.parse(parent_path.joinpath("sample.xml"))
root = tree.getroot()

for child in root:
    print(child.tag, child.attrib)