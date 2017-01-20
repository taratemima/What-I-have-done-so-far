from code_to_fix import bag_of_words
from lxml import etree

import FrequencySummarizer


def transform_and_edit(xml_file, xsl_file, search_term, new_sub_element):
    transformed_input = transform_file(xml_file, xsl_file)
    transform_tree = add_subelement(transformed_input, new_sub_element)
    transform_tree = add_results(transform_tree, new_sub_element, search_term)
    new_file = create_new_file_name(xml_file)
    write_complete_file(new_file, transform_tree)


def output_check(transform_tree, search_term):
    for element in transform_tree:
        for found in element.findall(search_term):
            if found.count(' ') < 1000:
                clean_text = normalize(found)
                # use found in keyword extraction and ranking
                available_words = bag_of_words.create_bag_of_words(clean_text)
                return clean_text, available_words
            else:
                clean_text = normalize(found)
                fs = FrequencySummarizer.FrequencySummarizer()
                short_text = fs.summarize(clean_text, 1)
                # use short_text in keyword extraction and ranking
                available_words = bag_of_words.create_bag_of_words(clean_text)
                return short_text, available_words


def transform_file(xml_file, xsl_file):
    parsed_xsl = etree.parse(xsl_file)
    parsed_xml = etree.parse(xml_file)
    transform = etree.XSLT(parsed_xsl)
    return transform(parsed_xml)


def add_subelement(transformed_input, new_subelement):
    transformed_tree = etree.parse(etree.ElementTree(transformed_input))
    etree.SubElement(transformed_tree, new_subelement)
    return transformed_tree


def add_results(transformed_tree, new_subelement, search_term):
    for element in transformed_tree:
        for found_words in element.findall(search_term):
            summary = summarize(found_words.text)
            transformed_tree.text[new_subelement] = summary
    return transformed_tree


def create_new_file_name(xml_file):
    return str(xml_file) + 'transformadded.xml'


def write_complete_file(new_file, transformed_tree):
    outfile = open(new_file, 'w')
    transformed_tree.write(outfile)
