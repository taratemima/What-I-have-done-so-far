# -*- coding: utf-8 -*-

import text_cleanup
from models import *
import peewee as pw
import csv
from collections import defaultdict
import os


# dirsWithXML = ['ipa141218', 'ipa141225', 'ipa150101', 'ipa150108', 'ipa150115', 'ipa150122',
#                'ipa150129', 'ipa150205', 'ipa150212', 'ipa150219', 'ipa150226', 'ipa150305',
#                'ipa150312', 'ipa150319', 'ipa150326', 'ipa150402', 'ipa150409', 'ipa150416',
#                'ipa150423', 'ipa150430', 'ipa150507', 'ipa150514', 'ipa150521', 'ipa150528',
#                'ipa150604', 'ipa150611', 'ipa150618', 'ipa150625', 'ipa150702', 'ipa150709',
#                'ipa150716', 'ipa150723', 'ipa150730', 'ipa150806', 'ipa150813', 'ipa150820',
#                'ipa150827', 'ipa150903', 'ipa150910', 'ipa150917', 'ipa150924', 'ipa151001',
#                'ipa151008', 'ipa151015', 'ipa151022', 'ipa151029', 'ipa151105', 'ipa151112',
#                'ipa151119', 'ipa151126', 'ipa151203', 'ipa151210', 'ipa151217', 'ipa151224',
#                'ipa151231', 'ipa160107', 'ipa160114', 'ipa160121', 'ipa160128', 'ipa160204',
#                'ipa160211', 'ipa160218', 'ipa160225', 'ipa160303', 'ipa160310', 'ipa160317',
#                'ipa160324', 'ipa160331', 'ipa160407', 'ipa160414', 'ipa160421', 'ipa160428',
#                'ipa160505', 'ipa160512', 'ipa160519', 'ipa160526', 'ipa160602', 'ipa160609',
#                'ipa160616', 'ipa160623', 'ipa160630',
#                'ipa160707', 'ipa160714', 'ipa160721', 'ipa160728', 'ipa160804', 'ipa160811',
#                'ipa160818', 'ipa160825', 'ipa160901', 'ipa160908', 'ipa160915', 'ipa160922',
#                'ipa160929', 'ipa161006', 'ipa161013', 'ipa161020', 'ipa161027', 'ipa161103']

def create_stemmed_samples(text):
    normalized_text = text_cleanup.normalize(text)
    return text_cleanup.stem_word_list(normalized_text)


def grab_records():
    abstract_words = []
    claim_words = []
    patent_ids = []
    try:
        # patentsToRequest = 100000
        #
        # patentsToRequest = 100
        patentsToRequest = 2
        myPatents = PatentClean.select(PatentClean.Patent,
                                       PatentClean.Abstract, PatentClean.Claim1).limit(patentsToRequest)

        # saved_patents = []

        # print "Requesting " + str(patentsToRequest) + " records."
        # print "Gained "+str(len(myPatents))+" records "

        for p in myPatents:
            abstract_words.extend(create_stemmed_samples(p.Abstract))
            claim_words.extend(create_stemmed_samples(p.Claim1))
            patent_ids.append(p.Patent)

        abstract_words = sorted(list(set(abstract_words)))
        claim_words = sorted(list(set(claim_words)))
        patent_ids = sorted(patent_ids)
        return abstract_words, claim_words, patent_ids
    except Exception, e:
        print "grab records"
        print str(e)
        pass


def create_abstract_storages(patent_id_list, words):
    patent_abstract_count = {}
    try:
        for patent in patent_id_list:
            indiv_patent = PatentClean.get(PatentClean.Patent == patent)
            for w in words:
                patent_abstract_count.setdefault((patent, w), 0)
                for entry in create_stemmed_samples(indiv_patent.Abstract):
                    if entry == w and (patent, entry) in patent_abstract_count:
                        patent_abstract_count[(patent, entry)] += 1
        return patent_abstract_count

    except Exception, e:
        print "create abstract storages"
        print str(e)
        pass


def create_claim_storages(patent_id_list, words):
    patent_claim_count = {}
    try:
        for patent in patent_id_list:
            indiv_patent = PatentClean.get(PatentClean.Patent == patent)
            for w in words:
                patent_claim_count.setdefault((patent, w), 0)
                for entry in create_stemmed_samples(indiv_patent.Claim1):
                    if entry == w and (patent, entry) in patent_claim_count:
                        patent_claim_count[(patent, entry)] += 1
        return patent_claim_count
        # print indiv_patent.Patent, entry
        # for word in words_dict.keys():
        #     patent_abstract_count[patent] [word] = 0

    except Exception, e:
        print "create claim storages"
        print str(e)
        pass


def create_matrix_from_dict(example_dict):
    sorted_docs = sorted(set(t[0] for t in example_dict))
    sorted_kwds = sorted(set(t[1] for t in example_dict))
    yield [None, ] + sorted_kwds
    for d in sorted_docs:
        yield [d, ] + [example_dict.get((d, k), 0) for k in sorted_kwds]



def create_csv_file(file_name, available_dict):
    os.chdir('C:/Users/Tara/PyCharmProjects/untitled/csv_results')
    with open(os.path.join('C:/Users/Tara/PyCharmProjects/untitled/csv_results/', file_name),
              'wb') as csvfile:
        w = csv.writer(csvfile)
        for key, value in available_dict.items():
            separate_keys = list(key)
            w.writerow([separate_keys[0], separate_keys[1], value])

            # w = csv.writer(csvfile)
            # w.writerows(available_dict.items())
            # csvwriter = csv.writer(csvfile, delimiter=',')
            # csvwriter.writerows(multiple_rows)


abstracts, claims, patent_ids = grab_records()
pre_csv_abstract_storage = create_abstract_storages(patent_ids, abstracts)
pre_csv_claim_storage = create_claim_storages(patent_ids, claims)
claims_sorted = create_matrix_from_dict(pre_csv_claim_storage)
abstracts_sorted = create_matrix_from_dict(pre_csv_abstract_storage)
create_csv_file("abstract6.csv", pre_csv_abstract_storage)
create_csv_file("claims6.csv", pre_csv_claim_storage)

# for row in create_matrix_from_dict(pre_csv_claim_storage):
#     print row
#
# for r in create_matrix_from_dict(pre_csv_abstract_storage):
#     print r


# I will now need to print the value of the key
