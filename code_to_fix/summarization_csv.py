import csv
import os
from xml.etree.ElementTree import parse
import io
import FrequencySummarizer
from sumy.parsers.plaintext import PlaintextParser  # We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer  # We're choosing Lexrank, other algorithms are also built in
from sumy.summarizers.text_rank import TextRankSummarizer


# dirWithXML = 'ipg160830'
dirWithXML = 'transformedReed'
baseDir = 'C:/Users/Tara/PycharmProjects/untitled/moreToTransform/' + dirWithXML + '/'  # directory with transformed xml file directories
# projRootDir = 'c:/gitProjects/From.XML.to.CSV'
projRootDir = baseDir


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


def testing_length(file_name, search_term):
    try:
        ucid, extracted_text, search_term = extracting_ucid_and_text(file_name, search_term)
        if extracted_text.count(' ') > 1000:
            testing_summarizers(extracted_text)
        else:

            # print "Original text in {}: {}".format(ucid, extracted_text)
            testing_summarizers(extracted_text)
    except TypeError:
        pass
    except UnicodeEncodeError:
        pass


def summarization_test():
    os.chdir(baseDir)
    for file_found in [f for f in os.listdir(baseDir) if f.endswith('xml')]:
        testing_length(file_found, 'abstract')


def testing_summarizers(extracted_text):
    parser = PlaintextParser.from_string(extracted_text, Tokenizer("english"))
    fs = FrequencySummarizer.FrequencySummarizer
    lrs = LexRankSummarizer()
    trs = TextRankSummarizer()
    summary1 = fs.summarize(fs, extracted_text, 1)
    summary2 = lrs(parser.document, 1)
    summary3 = trs(parser.document, 1)
    print "Frequency summarizer result: {}".format(summary1)
    print "Lex Rank summarizer result: {}".format(summary2)
    print "Text Rank summarizer result: {}".format(summary3)

summarization_test()
