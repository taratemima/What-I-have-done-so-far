import csv

from nltk import FreqDist

import bag_of_words
import growTree
import transform_guide


def create_transformed_tree(xml, xsl):
    transform_guide.transform_and_edit(xml, xsl)
    transformed_file = transform_guide.create_new_file_name(xml)
    return growTree.grow_tree(transformed_file)


def create_bag_from_file(transformed_tree):
    fdist1 = FreqDist()
    # search_terms = ['abstract', 'claim1Text', 'allClaimsText']
    # for term in search_terms:
    for match in transformed_tree.findall('abstract'):
        clean_text_list = bag_of_words.normalize(match.text)
        fdist1 = FreqDist(clean_text_list)
    # fdist1 |= fdist2
    return fdist1.most_common()


def grab_patent_numbers(transformed_tree):
    term = "ucid"
    patent_numbers = list()
    for match in transformed_tree.findall(term):
        patent_numbers.append(match)
    return patent_numbers


def create_csv_file(patent_numbers_from_xml, frequency_from_xml):
    with open('somePatentNumbers.csv', 'wb') as f:
        writer = csv.writer(f, dialect='tab-excel')
        writer.writerows(patent_numbers_from_xml)
        #writer.writerows(frequency_from_xml)



    def main_maker(xml_file, xsl_file):
        transformed_tree_root = create_transformed_tree(xml_file, xsl_file)
        print transformed_tree_root
        #bag_dict = create_bag_from_file(transformed_tree_root)
        #patent_number_list = grab_patent_numbers(transformed_tree)
        #grab_patent_numbers(transformed_tree_root)
        #create_csv_file(patent_number_list, bag_dict)

    main_maker('US-6186162-B1.xml', 'new_patents.xsl')
        # def work_from_folders(folder):
        #     for file_found in [f for f in os.listdir(folder) if f.endswith('.xml')]:
        #         main_maker(file_found, "new_patents.xsl")
        #
        # work_from_folders("C:/Users/Tara/PycharmProjects/untitled")
