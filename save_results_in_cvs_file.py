from nltk.corpus import stopwords
import re
import csv
from nltk import FreqDist
import os
from xml.etree.ElementTree import parse
import errno
import io
import sys

stopset = list(set(stopwords.words('english')))
legal_words = ['one','first','second','system','also','using','used','within','two','provide','according','provides','described','element','embodiment','via','non','whether','herein','application','e','third','without','g','respectively','less','b','c','means','allows','therein','thus','n','new','among','enable','obtain','define','novel','sample','pre','even','ii','effect','near','obtaining','allowing','x','resulting','select','p','r','anti','added','per','known','etc','item','accordingly','iii','ue','improving','relating','f','h','l','several','cm','id','problem','k','art','followed','mm','z','ones','bi','optimal','take','introducing','takes','u','advantageously','configure','provider','development','poly','difficult','enhancement','q','yet','achieving','chosen','decreases','essentially','fifth','wt','act','arrangements','issues','best','possibility','rather','require','satisfy','satisfying','similarly','aid','aware','called','hence','much','occurred','others','seen','abc','abl','said','either','thereof','wherein','may','whereby','whereinto','whereas','whereupon','whereafter']

stopset.extend(legal_words)
# reload(sys).setdefaultencoding("ISO-8859-1")


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

# The folder: C:/Users/Tara/PyCharmProjects/untitled/transformed_files
# multiple_tags = ['abstract', 'claim1Text', 'allClaimsText']
# I will need to make a dictionary to track tags and words associated with them


# def keys_to_skip(storage):
#     available_keys = storage.keys()
#     for a in available_keys:
#         if a.startswith('D'):
#             del storage[a]
#     return storage
# skip ucids that start with D
# skip files that bring up an error message


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


def create_tree(xml_file):
    with open(xml_file, mode='rb') as fp:
        tree = parse(fp)
        return tree.getroot()


def extract_results(xml_file, search_term):
    ucid = ""
    normalized_text = ""
    transform_tree = create_tree(xml_file)
    for patent in transform_tree.iter('patent-info'):
        ucid = patent.find('ucid').text
        for entry in patent.findall(search_term):
            normalized_text = normalize(entry.text)
    return ucid, normalized_text, search_term


# def create_frequency(cleaned_text):
#     fdist = FreqDist(cleaned_text)
#     tuple_list = fdist.most_common()
#     return ','.join('%s,%s' % tup for tup in tuple_list)


def create_frequency(cleaned_text):
   fdist = FreqDist(cleaned_text)
   return ','.join('%s,%s' % (key, str(value)) for (key, value) in sorted(fdist.items()))


# from http://stackoverflow.com/questions/3292643/python-convert-list-of-tuples-to-string


def add_to_storage(xml_file, search_term, storage):
    # os.chdir('C:/Users/Tara/PyCharmProjects/untitled/transformed_files')

    """

    :param search_term: string
    :param xml_file: file object
    :type storage: dict
    """

    ucid, normalized_text, search_term = extract_results(xml_file, search_term)

    if ucid.startswith('D'):
        return storage
    else:
        frequency = create_frequency(normalized_text)
        storage.update(store_results(search_term, ucid, frequency))
        return storage


# def filter_tree(file_found):
#     tree = create_tree(file_found)
#     for patent in tree.iter('patent-info'):
#         ucid = patent.find('ucid').text
#         if ucid.startswith('D'):
#             print "{} is not needed".format(file_found)
#             # write_csv_file(file_found)
#         else:
#             print "{} is available".format(file_found)


def storage_from_files():
    search_terms = ['abstract', 'claim1Text', 'allClaimsText']
    storage = dict()
    os.chdir('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed')
    for file_found in [f for f in os.listdir('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed/') if f.endswith('xml')]:
        for s in search_terms:
            storage = add_to_storage(file_found, s, storage)
            # storage = keys_to_skip(storage)
    return storage


def print_test():
    collected_results = storage_from_files()
    key_index = collected_results.keys()
    os.chdir('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed')
    # for k in key_index:
    #     print "{} is entered into the dictionary".format(k)
    print csv.field_size_limit()


def write_csv_file(csv_file):
        collected_results = storage_from_files()
        key_index = collected_results.keys()
        file_check()
        os.chdir('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed')
        with open(os.path.join('C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/transformedReed/', csv_file), 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            for k in key_index:
                all_entries = collected_results[k]
                csvwriter.writerow([all_entries[0], all_entries[1], all_entries[2]])

#print_test()
write_csv_file('collected4_ipg160830.csv')


