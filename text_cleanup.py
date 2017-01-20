from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import FreqDist
import re 

projRootDir = 'C:/Users/Tara/PycharmProjects/untitled'


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
    return sorted(fdist.items())
    # return ','.join('%s,%s' % (key, str(value)) for (key, value) in sorted(fdist.items()))
