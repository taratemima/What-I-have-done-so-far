import os
from xml.etree.ElementTree import parse
import io
from nltk.corpus import stopwords
import re
import csv
from nltk import FreqDist
import sys


stopset = list(set(stopwords.words('english')))
legal_words = ['said', 'either', 'thereof', 'wherein', 'may', 'whereby', 'whereinto', 'whereas', 'whereupon',
               'whereafter']
stopset.extend(legal_words)
reload(sys).setdefaultencoding("ISO-8859-1")
search_terms = ['abstract', 'claim1Text', 'allClaimsText']


def create_tree(xml_file):
    with io.open(xml_file, mode='rb') as fp:
        tree = parse(fp)
        return tree.getroot()


def filter_tree(file_found):
    tree = create_tree(file_found)
    for patent in tree.iter('patent-info'):
        ucid = patent.find('ucid').text
        if ucid.startswith('D'):
            print "{} is not needed".format(file_found)
        else:
            print "{} is needed".format(file_found)


def revised_folders():
    folder = "C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed"
    os.chdir(folder)
    for file_found in os.listdir(folder):
        if file_found.endswith('xml'):
            try:
                filter_tree(file_found)
                for s in search_terms:
                    extract_results(file_found, s)
            except UnicodeDecodeError:
                print "{} has bad characters".format(file_found)
            except TypeError:
                print "{} returned a different type".format(file_found)
            except AttributeError:
                print "{} is a different attribute".format(file_found)


def file_check():
    max_int = sys.maxsize
    decrement = True
    while decrement:
        decrement = False
        try:
            csv.field_size_limit(max_int)
        except OverflowError:
            max_int = int(max_int/10)
            decrement = True


def normalize(original_text):
    only_words = re.sub("[^a-zA-Z]", " ", original_text)
    lower_case = only_words.lower()  # Convert to lower case
    words = lower_case.split()  # Split into words
    return list([word for word in words if word not in stopset])


def store_results(search_term, ucid, frequency_text):
    storage = dict()
    # a dictionary of lists
    new_key = ucid+"_"+search_term
    storage[new_key] = [ucid, search_term, frequency_text]
    return storage


def extract_results(xml_file, search_term):
    transform_tree = create_tree(xml_file)
    # normalized_text = ""
    for patent in transform_tree.iter('patent-info'):
        ucid = patent.find('ucid').text
            # for entry in patent.findall(search_term):
            # normalized_text = normalize(entry.text)
        if ucid == "":
            print "{} has not found UCID".format(xml_file)
        else:
            print "{} can be used for {}".format(ucid, search_term)


def create_frequency(cleaned_text):
    fdist = FreqDist(cleaned_text)
    return ','.join('%s %s' % (key, str(value)) for (key, value) in sorted(fdist.items()))

def write_csv_file(csv_file):
    os.chdir('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed')
    with open(os.path.join('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed/', csv_file), 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        try:
            for k in key_index:
                all_entries = collected_results[k]
                csvwriter.writerow([all_entries[0], all_entries[1], all_entries[2]])
        except UnicodeDecodeError:
            print "File is not found"
        except AttributeError:
            print "Did not return what was expected."

# revised_folders()
