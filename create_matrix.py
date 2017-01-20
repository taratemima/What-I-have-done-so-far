# from itertools import chain
from collections import defaultdict
from models import Patent
from nltk.stem.snowball import SnowballStemmer
import text_cleanup

all_documents = list()
individual_patent = Patent()
ucid = individual_patent.ucid
claim_text = individual_patent.allClaimsText
# document_word_list = text_cleanup.normalize(claim_text)

# to do: refactor code in original_code_with_alphabetization so that both
# the matrix and the csv writer can use the same functions for normalizing,
# editing stopwords, and creating a stemmed list.

patentsToRequest = 100000
myPatents = individual_patent.select(ucid, claim_text).limit(patentsToRequest)

count = 0
print "Requesting " + str(patentsToRequest) + " records."

# Get data records
# Normalize claims text
# Create stemmed words list out of normalized claims text
# Create a frequency dictionary
# Store frequency dictionary with ucid as primary key
# Create stemmed words list as columns
# Create list of ucids as rows
# Create matrix of rows and columns
# Add frequency for word per ucid to value of row and column
# Write the result to a CSV file

#

# all_stems = stem_word_list(document_word_list)
# document_word_count = create_frequency(all_stems)
# stem_count = 0




# columns = list(set(list(chain(romeo.keys(), caesar.keys()))))
# rows = list(set(list(all_documents)))
# columns = list(set(list(document_word_count.keys())))
#
#
# matrix = defaultdict(dict)

# for coll in ('romeo', 'caesar'):
#     matrix[coll] = {}
#     for key in columns:
#         if dicts[coll].has_key(key):
#             matrix[coll][key] = dicts[coll][key]
#         else:
#             matrix[coll][key] = 0
#
# print columns

# for r in rows:
#     matrix[r] = {}
#     for key in columns:
#         if r in matrix:
#             new_count = document_word_count[r][key] + matrix[r][key]
#             matrix[r][key] = new_count
#         else:
#             matrix[r][key] = document_word_count[r][key]
#
# print columns
#
#
# for coll in matrix.keys():
#     for key in columns:
#         print matrix[coll][key],
#     print '\n'


 # Classes_dataset = {
 #        'description': 'CPC Classes',
 #        'relation': 'Classes',
 #        'attributes': [
 #            ('ClassMain', 'STRING'),
 #            ('ClassFurther', 'STRING'),
 #        ],
 #        'data': [
 #            ['F01N', 'F02D'],
 #            ['F01N', 'F02B'],
 #            ['F01N', 'Y02T'],
 #            ['F01N', 'B01D']
 #        ]
 #    }

#     Classes_dataset['data'][:] = []
#     ClassMainList = []
#     ClassFurtherList = []
#
#
#
#     for p in myPatents:
#         if p.CPCmain and p.CPCfurther:
#             #print "main: " + p.CPCmain + ", Fur:" + p.CPCfurther
#             count = count + 1
#             for cpcFurtherClass in [x.strip() for x in p.CPCfurther.split(',')]:
#                 Classes_dataset['data'].append([p.CPCmain, cpcFurtherClass])
#                 ClassFurtherList.append(cpcFurtherClass)
#                 ClassMainList.append(p.CPCmain)
#                 print "main: " + p.CPCmain + ", Fur:" + cpcFurtherClass
#
#     print "Received " + str(count) + " records with a CPC Main and Further class."
#
#     Classes_dataset['attributes'] = [
#             ('ClassMain', list(set(ClassMainList))),
#             ('ClassFurther', list(set(ClassFurtherList)))]
#
#     # http://stackoverflow.com/questions/25916731/how-to-write-in-arff-file-using-liac-arff-package-in-python
#     f = open('trainarff.arff', 'wb')
#     arff.dump(Classes_dataset, f)
#     f.close()
#
#     print "bob: " + str(Classes_dataset['data'])
# except Exception, e:
#     print "makeARFF: " + str(e)
#     pass
