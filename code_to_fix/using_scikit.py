from sklearn.feature_extraction.text import CountVectorizer

# Initialize the "CountVectorizer" object, which is scikit-learn's
# bag of words tool.
vectorizer = CountVectorizer(analyzer="word", \
                             tokenizer=None, \
                             preprocessor=None, \
                             stop_words=None, \
                             max_features=5000)


def create_input(file_name, search_term):
    pass
    # try:
    #     found_words = bag_of_words.prepare_answers_from_XML(file_name, search_term)
    #     #return bag_of_words.create_input_for_countvector(found_words, search_term)
    # except TypeError as (errno, strerror):
    #     print "Type error({0}): {1}".format(errno, strerror)



def work_from_folders(folder):
    pass
#     for file_found in [f for f in os.listdir(folder) if f.endswith('.xml')]:
#         search_terms = ['abstract', 'claim']
#         for s in search_terms:
#             from_file_to_input = create_input(file_found, s)
#             # fit_transform() does two functions: First, it fits the model
#             # and learns the vocabulary; second, it transforms our training data
#             # into feature vectors. The input to fit_transform should be a list of
#             # strings.
#             train_data_features = vectorizer.fit_transform(from_file_to_input)
#             # Numpy arrays are easy to work with, so convert the result to an
#             # array
#             train_data_features = train_data_features.toarray()
#             print train_data_features.shape
# work_from_folders('C://Users/Tara/PycharmProjects/untitled')