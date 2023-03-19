name_cnt ={}
def complex_dict_to_flat(data, output = {}, name = ""):
    # todo: dictではないときにエラーを返そう。try ~ catch構文を使用できない？
    if type(data) is dict:
        for key in data.keys():
            dict_val = data[key]
            if type(dict_val) is dict:
                output = complex_dict_to_flat(dict_val, output, name+key+".")
            elif type(dict_val) is list:
                for item in dict_val:
                    output = complex_dict_to_flat(item, output, name+key+".")
            # If it is a value, register it as a dictionary value for output
            else:
                # If the common parts of the keys are the same, add a suffix to make them unique. 
                key_common_part = name + key
                if key_common_part in output.keys():
                    count = name_cnt[key_common_part] = name_cnt.get(key_common_part, 0) + 1
                    output[key_common_part+'.'+str(count)] = dict_val
                else:
                    output[key_common_part] = dict_val

    return output

def convert_elem_dict(node):
    result = {}

    # get attribute name and value.
    if node.attrib:
        result['@attribs'] = dict(node.items())

    for element in node:
        key = element.tag

        # When text is present and not empty, get text.
        # To prevent errors, use strip only when text is present.
        if element.text and element.text.strip():
            value = element.text

        # hack: The following should be done even when there are both text nodes and child nodes.
        else:
            value = convert_elem_dict(element)

        # If there are multiple nodes with the same name in the same hierarchy, their values in dictionary are retained in a list.
        """
        Below is an example.
        Two "country nodes" are in the same hierarchy and their values are stored in a list.
        [input]
        <data>
            <country name="china" />
            <country name="korea" />
        </data>

        [output]
        {'country': [{'@attribs': {'name': 'china'}}, {'@attribs': {'name': 'korea'}}]}
        """
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


import xml.etree.ElementTree as ET
def parse():
    root = ET.parse('./src/xmlparser/sample_text_node.xml').getroot()
    xmlDict = convert_elem_dict(root)
    from pprint import pprint
    pprint(xmlDict)
    
    response = complex_dict_to_flat(xmlDict)
    return response

import csv
def main():
    result = parse()

    with open("output.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, result.keys()) 
        writer.writeheader()
        writer.writerow(result)

if __name__ == '__main__':
    main()