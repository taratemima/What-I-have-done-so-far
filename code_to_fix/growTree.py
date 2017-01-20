from lxml import etree

def grow_tree(file_listed):
    tree = etree.parse(file_listed)
    root = tree.getroot()
    return root
