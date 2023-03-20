"""
convert xml to csv.
"""

import xml.etree.ElementTree as ET
import csv
import sys

name_cnt ={}
def nested_dict_to_flat(data, output = {}, name = ""):
    """change nested dictionary to flat dictionary."""
    if type(data) is dict:
        for key in data.keys():
            dict_val = data[key]
            if type(dict_val) is dict:
                output = nested_dict_to_flat(dict_val, output, name+key+".")
            elif type(dict_val) is list:
                for item in dict_val:
                    output = nested_dict_to_flat(item, output, name+key+".")
            # If it is a value, register it as a dictionary value for output
            else:
                # If the common parts of the keys are the same, add a suffix to make them unique. 
                key_common_part = name + key
                if key_common_part in output.keys():
                    count = name_cnt[key_common_part] = name_cnt.get(key_common_part, 0) + 1
                    output[key_common_part+'.'+str(count)] = dict_val
                else:
                    output[key_common_part] = dict_val
    else:
        print("type of input is wrong. exit.")
        sys.exit()

    return output

name_cnt ={}
def nested_dict_to_list(data, output = {}, name = ""):
    """change nested dictionary to flat dictionary."""
    if type(data) is dict:
        for key in data.keys():
            dict_val = data[key]
            if type(dict_val) is dict:
                output = nested_dict_to_list(dict_val, output, name+key+".")
            elif type(dict_val) is list:
                for item in dict_val:
                    output = nested_dict_to_list(item, output, name+key+".")
            # If it is a value, register it as a dictionary value for output
            else:
                # If the common parts of the keys are the same, add a suffix to make them unique. 
                key_common_part = name + key
                if key_common_part in output.keys():
                    count = name_cnt[key_common_part] = name_cnt.get(key_common_part, 0) + 1
                    output[key_common_part+'.'+str(count)] = dict_val
                else:
                    output[key_common_part] = dict_val
    else:
        print("type of input is wrong. exit.")
        sys.exit()

    return output

def convert_elem_dict(node):
    """convert element tree to dictionaries."""
    result = {}

    # get attribute name and value.
    if node.attrib:
        result['@attribs'] = dict(node.items())

    for element in node:
        key = element.tag

        # When text is present and not empty, get text.
        if element.text:
            if element.text.strip():
                value = element.text
            else:
                value = convert_elem_dict(element)

        # If there are multiple nodes with the same name in the same hierarchy, their values in dictionary are retained in a list.
        #Below is an example.
        #Two "country nodes" are in the same hierarchy and their values are stored in a list.
        #[input]
        #<data>
        #    <country name="china" />
        #    <country name="korea" />
        #</data>
        #[output]
        #{'country': [{'@attribs': {'name': 'china'}}, {'@attribs': {'name': 'korea'}}]}
        if key in result:
            if type(result[key]) is not list:
                # When it finds a second node with the same name, it stores them in a list.
                first_node_value = result[key].copy()
                result[key] = [first_node_value, value]
            else:
                # When the third and subsequent nodes with the same name are found, they are added to the existing list.
                result[key].append(value)
        else:
            result[key] = value

    return result

def parse_xml():
    root = ET.parse('./src/xmlparser/sample_text_node.xml').getroot()
    xmlDict = convert_elem_dict(root)
    from pprint import pprint
    pprint(xmlDict)
    
    response = nested_dict_to_flat(xmlDict)
    return response

def main():
    result = parse_xml()

    with open("output.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, result.keys()) 
        writer.writeheader()
        writer.writerow(result)

if __name__ == '__main__':
    main()