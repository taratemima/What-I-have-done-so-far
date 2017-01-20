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
import FrequencySummarizer

dirWithXML = 'ipg160830'
baseDir = 'C:/Users/Tara/PycharmProjects/untitled/moreToTransform/' + dirWithXML +'/' #directory with transformed xml file directories
projRootDir = 'c:/gitProjects/From.XML.to.CSV'


def stem_word_list(list_of_words):
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    stemmed_words = list()
    for word in list_of_words:
        stemmed_words.append(stemmer.stem(word))
    return stemmed_words


def creating_stop_words():
    stopset = list(set(stopwords.words('english')))

    legal_words = open(projRootDir + '/legal_words.txt', 'r')
    for line in legal_words.readlines():
        stopset.append(line.strip())
    return stopset


def normalize(original_text):
    stopset = creating_stop_words()
    only_words = re.sub("[^a-zA-Z]", " ", original_text)
    lower_case = only_words.lower()  # Convert to lower case
    words = lower_case.split()  # Split into words
    return list([word for word in words if word not in stopset])


def create_frequency(cleaned_text):
    fdist = FreqDist(cleaned_text)
    return ','.join('%s,%s' % (key, str(value)) for (key, value) in sorted(fdist.items()))


def create_tree(xml_file):
    os.chdir(baseDir)
    with io.open(xml_file, mode='rb') as fp:
        tree = parse(fp)
        return tree.getroot()


def store_results(search_term, ucid, altered_text):
    storage = dict()
    # a dictionary of lists
    new_key = ucid+"_"+search_term
    storage[new_key] = [ucid, search_term, altered_text]
    return storage


def extracting_ucid_and_text(xml_file, search_term):
    transform_tree = create_tree(xml_file)
    for patent in transform_tree.iter('patent-info'):
        try:
            ucid = patent.find('ucid').text
            extracted_text = patent.find(search_term).text
            return ucid, extracted_text, search_term
        except AttributeError:
            pass


def add_to_storage(xml_file, storage, search_term):
    try:
        ucid, available_text, search_term = extracting_ucid_and_text(xml_file, search_term)
        if ucid.startswith('D'):
            return storage
        else:
            cleaned_stemmed = normalize_and_stem(available_text)
            frequency = create_frequency(cleaned_stemmed)
            return update_with_stored_results(search_term, ucid, frequency, storage)
    except TypeError:
        pass


def update_with_stored_results(search_term, ucid, used_text, storage):
    storage.update(store_results(search_term, ucid, used_text))
    return storage


def search_and_store(xml_file, storage):
    search_terms = ['abstract', 'claim1Text', 'allClaimsText']
    for s in search_terms:
        add_to_storage(xml_file, storage, s)
    return storage


def normalize_and_stem(extracted_text):
    cleaned_text = normalize(extracted_text)
    return stem_word_list(cleaned_text)


def storage_from_files():
    storage = dict()
    os.chdir(baseDir)
    for file_found in [f for f in os.listdir(baseDir) if f.endswith('xml')]:
        storage = search_and_store(file_found, storage)
    return storage


def print_the_storage():
    os.chdir(baseDir)
    collected_results = storage_from_files()
    key_index = collected_results.keys()
    for k in key_index:
        print "{} with {}".format(k, collected_results[k])


def write_csv_file(csv_file):
    collected_results = storage_from_files()
    key_index = collected_results.keys()
    # #         file_check()
    os.chdir(baseDir)
    with open(baseDir + csv_file, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        try:
            for k in key_index:
                all_entries = collected_results[k]
                csvwriter.writerow([all_entries[0], all_entries[1], all_entries[2]])
        except UnicodeDecodeError:
            pass
        except UnicodeEncodeError:
            pass
#
#
write_csv_file(dirWithXML + '.csv')
# print_the_storage()
