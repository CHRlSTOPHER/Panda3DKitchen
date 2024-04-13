from lxml import etree as ET
from classes.apps import AppGlobals as AG

transform_data = {
    "pos": "0, 0, 0",
    "hpr": "0, 0, 0",
    "scale": "1, 1, 1",
    "color": "1, 1, 1, 1",
    'color_scale': "1, 1, 1, 1"
}

def load_xml(xml_file):
    # load xml in a way that allows for pretty print
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(xml_file, parser)
    root = tree.getroot()
    return tree, root

def delete_xml_entries(mode, names):
    split_names = [name.split('|') for name in names]
    mode_name = AG.FILE_MODES[mode]
    xml_file = f"{base.project_location}/{mode_name}.xml"
    tree, root = load_xml(xml_file)
    # run through all the elements
    for element in root:
        name = element.attrib['name']
        index = element.attrib['index']
        # keep track of which index is being matched with
        # remove the matched items from both lists to reduce the amount
        # of checks python has to do for future comparisons.
        i = 0
        # check if any of the discarded names match the element
        for dis_name, dis_index, dis_part in split_names:
            if name == dis_name and index == dis_index:
                # found a match. remove the element from the xml.
                root.remove(element)
                # remove the name from the split names.
                split_names.pop(i)
                break # check completed. go to the next element.
            i += 1

    tree.write(xml_file, pretty_print=True, encoding="utf-8")

def convert_string_to_tuple(string):
    split_string = string.split(',')
    transform = [int(num) for num in split_string]
    return transform

def get_node_data(xml_file):
    tree, root = load_xml(xml_file)
    node_list = {}
    # get each top level element (either actor or prop in this case)
    for element in root:
        name = element.attrib['name']
        index = element.attrib['index']

        transforms = []
        # get the transform data for each node part
        for node in element:
            for i in range(0, 5):
                transforms.append(convert_string_to_tuple(node[i].text))
            node_list[f"{name}|{index}|{node.tag}"] = transforms

    return node_list

def add_default_transform(root_node):
    for data in transform_data:
        transform = ET.SubElement(root_node, data)
        transform.text = transform_data[data]

def append_node_data(xml_file, node_type, item_name):
    tree, root = load_xml(xml_file)
    # check if instances of the node already exist
    instances = 0
    for child in root:
        name = child.attrib['name'] # get the name of the node
        if item_name in name: # check if there are other instances of it
            instances += 1 # if so, add to the counter

    # create a new prop / actor with a name and index
    item = ET.SubElement(root, node_type, name=item_name, index=f"{instances}")
    # Define the child sub element. Set it to none since this is the parent.
    root_node = ET.SubElement(item, 'root_node')
    add_default_transform(root_node)

    tree.write(xml_file, pretty_print=True, encoding="utf-8")