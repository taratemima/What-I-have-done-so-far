from nltk.corpus import stopwords
import re
import csv
from nltk import FreqDist
import os
from xml.etree.ElementTree import parse
import errno
import io
import sys
from nltk.stem.snowball import SnowballStemmer
import FrequencySummarizer as fs


def creating_stop_words():
    stopset = list(set(stopwords.words('english')))
    os.chdir('C:/Users/Tara/PycharmProjects/untitled')
    legal_words = open("C:/Users/Tara/PycharmProjects/untitled/legal_words.txt", 'r')
    for line in legal_words.readlines():
        stopset.append(line.strip())
    return stopset


def stem_word_list(list_of_words):
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    stemmed_words = list()
    for word in list_of_words:
        stemmed_words.append(stemmer.stem(word))
    return stemmed_words


def normalize(original_text):
    stopset = creating_stop_words()
    only_words = re.sub("[^a-zA-Z]", " ", original_text)
    lower_case = only_words.lower()  # Convert to lower case
    words = lower_case.split()  # Split into words
    return list([word for word in words if word not in stopset])


def claim_text_frequency(original_text):
    original_list = normalize(original_text)
    stem_list = stem_word_list(original_list)
    return create_frequency(stem_list)


def create_frequency(cleaned_text):
    fdist = FreqDist(cleaned_text)
    return ','.join('%s %s' % (key, str(value)) for (key, value) in sorted(fdist.items()))
#     # return ','.join('%s,%s' % tup for tup in tuple_list)
#


def create_tree(xml_file):
    with open(xml_file, mode='rb') as fp:
        tree = parse(fp)
        return tree.getroot()


def store_results(search_term, ucid, altered_text):
    storage = dict()
    # a dictionary of lists
    new_key = ucid+"_"+search_term
    storage[new_key] = [ucid, search_term, altered_text]
    return storage


def testing_length(original_text):
    if original_text.count(' ') > 1000:
        new_text = fs.summarize(original_text, 1)
    else:
        new_text = original_text
    return new_text


def extracting_ucid_and_text(xml_file, search_term):
    ucid = ""
    extracted_text = ""
    transform_tree = create_tree(xml_file)
    for patent in transform_tree.iter('patent-info'):
        ucid = patent.find('ucid').text
        extracted_text = patent.find(search_term).text
    return ucid, extracted_text, search_term


def add_to_storage(xml_file, storage, search_term):
    ucid, available_text, search_term = extracting_ucid_and_text(xml_file, search_term)
    storage.update(store_results(search_term, ucid, available_text))
    return storage


def extract_abstract_results(xml_file):
    search_term = 'abstract'
    ucid, original_text, search_term = extracting_ucid_and_text(xml_file, search_term)
    abstract_text = testing_length(original_text)
    return ucid, abstract_text, search_term


def extract_frequency(xml_file):
    search_terms = ['claim1Text', 'allClaimsText']
    for search_term in search_terms:
        ucid, original_text, search_term = extracting_ucid_and_text(xml_file, search_term)
        stem_frequency_string = claim_text_frequency(original_text)
        return ucid, stem_frequency_string, search_term





# def new_functions_test():
#
#     os.chdir('C:/Users/Tara/PycharmProjects/untitled/moreToTransform/transformedReed')
#     for file_found in [f for f in os.listdir('C:/Users/Tara/PycharmProjects/untitled/moreToTransform/transformedReed/') if f.endswith('xml')]:
#         try:
#             ucid, abstract_text, search_term = extract_abstract_results(file_found)
#             storage = store_results(search_term, ucid, abstract_text)
#             #print "{} found with ucid {}, abstract {}, and {}".format(file_found, ucid, abstract_text, search_term)
#             for (key, value) in sorted(storage.items()):
#                 print (key, str(value))
#         except AttributeError:
#             print "Abstract not found"
#         except UnicodeEncodeError:
#             pass
#         except IOError:
#             print "Did not find entry"


# new_functions_test()

# complete_stopwords = creating_stop_words()
# for s in sorted(complete_stopwords):
#     print "{} is in list".format(s)
#
# # reload(sys).setdefaultencoding("ISO-8859-1")
#
#

#
#
# def file_check():
#     max_int = sys.maxsize
#     decrement = True
#     while decrement:
#         decrement = False
#         try:
#             csv.field_size_limit(max_int)
#         except OverflowError:
#             max_int = int(max_int/10)
#             decrement = True
#
# # The folder: C:/Users/Tara/PyCharmProjects/untitled/transformed_files
# # multiple_tags = ['abstract', 'claim1Text', 'allClaimsText']
# # I will need to make a dictionary to track tags and words associated with them
#
#
#

#

#
#
#
# # from http://stackoverflow.com/questions/3292643/python-convert-list-of-tuples-to-string
#
# def create_abstract_storage(ucid, text):
#     search_term = 'abstract'
#     storage = store_results(search_term, ucid, text)
#     return storage
#
#
#
# def extract_stemmed_results(xml_file, search_term):
#     ucid, original_text, search_term = extracting_ucid_and_text(xml_file, search_term)
#     stemmed_text = stem_word_list(normalize(original_text))
#     return ucid, stemmed_text, search_term
#
#

#
#
# def stemmed_add_to_storage(xml_file, search_term, storage):
#     # os.chdir('C:/Users/Tara/PyCharmProjects/untitled/transformed_files')
#
#     """
#
#     :param search_term: string
#     :param xml_file: file object
#     :type storage: dict
#     """
#
#     ucid, stemmed_text, search_term = extract_stemmed_results(xml_file, search_term)
#     frequency = create_frequency(normalized_text)
#     if ucid.startswith('D'):
#         return storage
#     else:
#         storage.update(store_results(search_term, ucid, frequency))
#         return storage
#
#
# def abstract_add_to_storage(xml_file, storage):
#     ucid, abstract_text, search_term = extract_abstract_results(xml_file)
#     storage.update(store_results(search_term, ucid, abstract_summary))
#     return storage
#
#
# def storage_from_files():
#     search_terms = ['claim1Text', 'allClaimsText']
#     storage = dict()
#     os.chdir('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed')
#     for file_found in [f for f in os.listdir('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed/') if f.endswith('xml')]:
#         storage = abstract_add_to_storage(file_found, storage)
#         for s in search_terms:
#             storage = stemmed_add_to_storage(file_found, s, storage)
#
#             # storage = keys_to_skip(storage)
#     return storage
#
#
# def write_csv_file(csv_file):
#         collected_results = storage_from_files()
#         key_index = collected_results.keys()
#         file_check()
#         os.chdir('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed')
#         with open(os.path.join('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed/', csv_file), 'wb') as csvfile:
#             csvwriter = csv.writer(csvfile, delimiter=',')
#             for k in key_index:
#                 all_entries = collected_results[k]
#                 csvwriter.writerow([all_entries[0], all_entries[1], all_entries[2]])
#
#
# def print_test():
#     collected_results = storage_from_files()
#     key_index = collected_results.keys()
#     os.chdir('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed')
#     for k in key_index:
#         print "{} is entered into the dictionary".format(k)
#     # print csv.field_size_limit()
#
# #print_test()
# # write_csv_file('collected4.csv')
