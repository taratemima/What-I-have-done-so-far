from sklearn.feature_extraction.text import CountVectorizer
import re
from nltk.corpus import stopwords

text = "He has short brown hair and brown eyes, with a curl on the left side of his head, which acts as his erogenous zone when stroked or pulled. He wears a blue WWII military uniform, a black shirt and tie, and black boots. In earlier strips, his hair was shown smoother, and his curl was drawn smaller, a change which was noted in a gag illustration. Italy's eyes were depicted as gray in the earliest artwork of him, but quickly changed to brown. In the Volume 5 Special Booklet, Himaruya notes that he's changed the way Italy's hair falls, and it now appears shorter and more spread out as opposed to longer and falling to the sides of his head."
stopset = list(set(stopwords.words('english')))

vectorizer = CountVectorizer(analyzer="word", \
                             tokenizer=None, \
                             preprocessor=None, \
                             stop_words=None, \
                             max_features=5000)


def normalize(original_text):
    # type: (string) -> string
    only_words = re.sub("[^a-zA-Z]", " ", original_text)
    lower_case = only_words.lower()  # Convert to lower case
    words = lower_case.split()  # Split into words
    total = list([word for word in words if word not in stopset])
    return " ".join(total)


total = (normalize(text),)
train_data_features = (vectorizer.fit_transform(total))
train_data_features = train_data_features.toarray()
print train_data_features.shape


def ranked_list(normalized_text):
    pass
    # create a dictionary of tokens as keys and count as values
    # arrange dictionary as descending rank of counts
    # return keys
