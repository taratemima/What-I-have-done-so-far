import os

from nltk import FreqDist

import FrequencySummarizer
import bag_of_words
import growTree

fs = FrequencySummarizer.FrequencySummarizer()


def testing_length(file_name, search_term):
    doc_root = growTree.grow_tree(file_name)
    new_text = ""

    for match in doc_root.findall(search_term):
        original_text = match.text
        if original_text.count(' ') > 1000:
            new_text = fs.summarize(original_text, 1)
        else:
            new_text = original_text
    return new_text


def create_bag_of_words(file_name):
    doc_root = growTree.grow_tree(file_name)
    fdist1 = FreqDist()
    search_terms = ['abstract', 'claim1Text','allClaimsText']
    for term in search_terms:
        for match in doc_root.findall(term):
            clean_text_list = bag_of_words.normalize(match.text)
            fdist2 = FreqDist(clean_text_list)
            fdist1 |= fdist2
    return fdist1.most_common()
    # get dictionary of count and tokens
    # sort by descending count
    # return string of descending tokens


def testing_the_output():
    print(create_bag_of_words('transformed_files/US-6186162-B1-transform.xml'))
    print (testing_length('transformed_files/US-6186162-B1-transform.xml', 'abstract'))
    print (testing_length('transformed_files/US-6186162-B1-transform.xml', 'allClaimsText'))

def work_from_folders(folder):
    for file_found in [f for f in os.listdir(folder) if f.endswith('.xml')]:
        print(create_bag_of_words(file_found))
        print testing_length(file_found, 'abstract')
        print testing_length(file_found, 'allClaimsText')

work_from_folders('C:/Users/Tara/PyCharmProjects/untitled')

#csv, patent number, abstract bag-of-words
#csv, patent number, claim1 bag-of-words
#csv, patent number, allclaims
#patent number; first word; first word frequency ...focus on abstract