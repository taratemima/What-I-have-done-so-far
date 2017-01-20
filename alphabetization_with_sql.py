# -*- coding: utf-8 -*-

import re
import csv
import os
from HTMLParser import HTMLParser
from xml.etree.ElementTree import parse
import errno
from lxml import etree
import io
import codecs
import sys
import FrequencySummarizer
from sumy.parsers.plaintext import PlaintextParser  # We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer # We're choosing Lexrank, other algorithms are also built in
from sumy.summarizers.text_rank import TextRankSummarizer
import text_cleanup


dirWithXML = 'NLCTestDataU'  # Also to be basis for csv file name
baseDir = 'C:/Users/Tara/PycharmProjects/untitled/moreToTransform/' + dirWithXML +'/' #directory with transformed xml file directories
projRootDir = 'c:/gitProjects/From.XML.to.CSV'



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

    #transform_tree = create_tree(xml_file)
    transform_tree = etree.parse(xml_file)
    for patent in transform_tree.iter('patent-info'):
        try:
            ucid = patent.find('ucid').text
            extracted_text = patent.find(search_term).text
            return ucid, extracted_text, search_term
        except AttributeError:
            pass

def get_values_from_xml_file(xml_file, list):
    """
    Given an xml file, pull out the element values in the list argument
    Modifies and returns passed in list
    From: http://stackoverflow.com/questions/7423118/python-list-for-each-access-find-replace-in-built-in-list
    :param xml_file: transformed xml file, list: list of tags whose values need to be retrieved from xml file
    :return: modified list with values from xml file
    """

    # todo: handle tags that doesn't exist, other error checking
    #f = codecs.open(xml_file, encoding='utf-8')
    try:

        #transform_tree = create_tree(xml_file)
        transform_tree = etree.parse(xml_file)
        for patent in transform_tree.iter('patent-info'):

            for ndx, member in enumerate(list):
                try:
                    value = patent.find(list[ndx]).text.encode('utf8')
                    list[ndx] = value
                except Exception, e:
                    print "get_values_from_xml_file inner: " + str(e)
                    list[ndx] = ""
            return list
    except Exception, e:
        print "get_values_from_xml_file: " + str(e)
        pass



def add_to_storage(xml_file, storage, search_term):
    try:
        ucid, available_text, search_term = extracting_ucid_and_text(xml_file, search_term)
        if ucid.startswith('D'):
            return storage
        else:
            cleaned_stemmed = normalize_and_stem(available_text)
            frequency = text_cleanup.create_frequency(cleaned_stemmed)
            return update_with_stored_results(search_term, ucid, frequency, storage)
    except TypeError:
        pass


def update_with_stored_results(search_term, ucid, used_text, storage):
    storage.update(store_results(search_term, ucid, used_text))
    return storage


def search_and_store(xml_file, storage, search_terms):
    for s in search_terms:
        add_to_storage(xml_file, storage, s)
    return storage


def normalize_and_stem(extracted_text):
    cleaned_text = text_cleanup.normalize(extracted_text)
    return text_cleanup.stem_word_list(cleaned_text)


def storage_from_files():
    storage = dict()
    os.chdir(baseDir)
    for file_found in [f for f in os.listdir(baseDir) if f.endswith('xml')]:
        storage = search_and_store(file_found, storage, ['abstract', 'claim1Text', 'allClaimsText'])
    return storage

def SummarizeAbstractToMaxLength(abstract, maxLength):
    parser = PlaintextParser.from_string(abstract, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    abstractSummary = summarizer(parser.document, 10)  # Summarize the document with N sentences
    abstract = unicode("")
    longFirstSentence = True
    # print abstract
    print "> " + str(maxLength) + " abstract"
    for sentence in abstractSummary:
        if (len(abstract) + len(unicode(sentence))) < maxLength:  # Trick to only add enough sentences to stay under 1024 chars
            longFirstSentence = False
            print "sentence"
            abstract += unicode(sentence)
        elif (len(unicode(sentence)) > maxLength) and longFirstSentence:
            print "Truncate long first sentence"
            abstract = unicode(sentence)[:maxLength]
            break

    return abstract.encode("utf-8")


def prepare_Abstract_for_NLC(ucid, abstract):
    # html = HTMLParser()

    #print "start length: " + str(len(abstract))
    abstract = abstract.encode("utf-8")
    abstract = ' '.join(abstract.split())  # Gets rid of whitespace
    #  http://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
    #abstract = abstract.replace('\r\n', ' ')
    #abstract = abstract.replace('\n', ' ').replace('\r', '')
    abstract = abstract.replace('', '').replace('', '').replace('', '')
    abstract = abstract.replace(", ", ",")  # replace comma space with just a comma

    #abstract = re.sub(r"(\(\d+\))", "", abstract)  # Remove all individual numbers inside of parens, will also include csv numbers in parens now

    # http://rubular.com/r/hUp4GQwMHE
    abstract = re.sub(r"(\([\d,]*\))", "", abstract)  # Remove all individual numbers inside of parens, will also include csv numbers in parens now
    abstract = re.sub(r"(\d+[a-zA-Z] )", "", abstract)  # Remove references like "10A " (with the space) from the text

    # See Granted patent: 09418453 pub date: 2016-08-16 for mathematical chars and how they come through
    # originally segment-4678.xml

    #  http://stackoverflow.com/questions/4876716/using-python-to-edit-html-but-lxml-converts-nice-html-entities-to-strange-encod
    # abstract = re.sub('&#(\d+);', lambda m: chr(int(m.group(1))).decode('cp1252'), abstract)

    #abstract = html.unescape(abstract)

    #print "end length: " + str(len(abstract))

    maxAbstractLength = 1020
    # todo: What if main sentence is longer than 1024 chars?


    # Delete stop words from abstract
    abstractStopped = text_cleanup.normalize(abstract)

    # Stem remaining words
    abstractStoppedStemmedList = text_cleanup.stem_word_list(abstractStopped)

    abstractStrStemmed = ' '.join(abstractStoppedStemmedList[:59])


    ###if len(abstract) > maxAbstractLength:
        # Make a function to lop off sentences if greater than 1024
        ### abstract = SummarizeAbstractToMaxLength(abstract, maxAbstractLength)
        ### print "summary length: " + str(len(abstract))
    ###else:
        ### print "got short abstract"

    if len(abstractStrStemmed) > maxAbstractLength:
        # Make a function to lop off sentences if greater than 1024
        abstract = abstractStrStemmed[:maxAbstractLength]
        print "summary length: " + str(len(abstract))
    else:
        abstract = abstractStrStemmed
        print "got short abstract"

    print "return abstract: " + ucid
    return abstract #.encode("utf-8")



def createLoadNLCDictionary():
    NLCdictionary = dict()  # main dictionary to hold each record(dictionary)
    os.chdir(baseDir)
    for file_found in [f for f in os.listdir(baseDir) if f.endswith('xml')]:
        try:
            # todo: look at segment-0618.xml from 07/26/2016, fix xsl to compensate
            patentValueList = get_values_from_xml_file(file_found, ['ucid', 'abstract', 'cpcMain'])
            ucid = patentValueList[0]

            if not (ucid.startswith('D') or ucid.startswith('PP') or ucid.endswith('SEQ')):  # if UCID starts with D (design) or send with SEQ (DNA sequence), then skip it
                NLCIndivRecord = dict()  # New dict to hold individual record from xml file

                #This would be the place to call the summarizer on the abstract: patentValueList[1]

                abstract = prepare_Abstract_for_NLC(ucid, patentValueList[1].decode('utf-8'))

                NLCIndivRecord[ucid] = [abstract.decode("utf-8"), patentValueList[2].decode('utf-8')]
                NLCdictionary.update(NLCIndivRecord)
                print "updated dictionary"
        except Exception, e:
            print " createLoadNLCDictionary: " + str(e)
            pass

    print "loop?"
    return NLCdictionary


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

def write_Watson_training_csv_file(csv_file):
    collected_results = createLoadNLCDictionary()  # dictionary of dictionaries
    key_index = collected_results.keys()

    with open(baseDir + csv_file, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        for k in key_index:
            try:

                #print "key index" + k
                all_entries = collected_results[k]
                csvwriter.writerow([all_entries[0].encode("utf-8"), all_entries[1].encode("utf-8")])
            except Exception, e:
                print "write_Watson_training_csv_file: " + k + ' ' + str(e)
                pass

#
# todo: spin through many subdirectories
#write_csv_file(dirWithXML + '.csv')


#This will be the Watson training file with summaries of abstracts in one column, cpcMain class in the second column
write_Watson_training_csv_file(dirWithXML + 'NLCtrain.csv')

# print_the_storage()
