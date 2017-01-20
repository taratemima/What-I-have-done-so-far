from nltk.corpus import stopwords
import re

stopset = list(set(stopwords.words('english')))


def normalize(original_text):
    # type: (string) -> list
    only_words = re.sub("[^a-zA-Z]", " ", original_text)
    lower_case = only_words.lower()  # Convert to lower case
    words = lower_case.split()  # Split into words
    return list([word for word in words if word not in stopset])


def create_string(original_text_list):
    return " ".join(original_text_list)
