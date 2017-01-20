from lxml import etree
import os


def transform_and_edit(xml_file, xsl_file):
    transformed_input = transform_file(xml_file, xsl_file)
    new_file = create_new_file_name(xml_file)
    write_complete_file(new_file, transformed_input)

def transform_file(xml, xsl):
    parsed_xsl = etree.parse(xsl)
    parsed_xml = etree.parse(xml)
    transform = etree.XSLT(parsed_xsl)
    return transform(parsed_xml)


def create_new_file_name(xml_file):
    original = os.path.splitext(xml_file)
    return str(original[0]+"transform.xml")


def write_complete_file(new_file, transformed_tree):
    outfile = open(new_file, 'w')
    transformed_tree.write(outfile)


def write_to_new_directory(folder, new_file, xml_file, xsl_file):
    new_path  = str(folder)+"/"+str(new_file)
    if os.path.exists(new_path):
        print "File already exists."
    else:
        transform_and_edit(xml_file, xsl_file)
