from xml.etree.ElementTree import parse

def length_result(entered_string):
    if entered_string.count('') > 20:
        print "Make it smaller"
    else:
        print entered_string

def tree_result(file_name, search_term):
    result_string = extract_text(file_name, search_term)
    length_result(result_string)

def extract_text(file_name, search_term):
    transform_tree = create_tree(file_name)
    for patent in transform_tree.iter('patent-info'):
        extracted_string = patent.find(search_term).text
    return extracted_string

def create_tree(xml_file):
    with open(xml_file, mode='rb') as fp:
        tree = parse(fp)
        return tree.getroot()
