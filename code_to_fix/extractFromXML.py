from code_to_fix import bag_of_words

import FrequencySummarizer
import growTree


def testing_length(file_listed, search_term):
    root = growTree.grow_tree(file_listed)
    #may need to change it to guiding transformation
    for abstract in root.findall(search_term):
        original_text = abstract.text
        print (original_text.count(''))
        # if original_text.count(' ') > 1000:
        #    print("This is a candidate for first summarization than bag of words extraction")
         #   fs.summarize(abstract.text,2)
        #else:
         #   print("This is a candidate for bag of words extraction")

            # print (abstract.text)

testing_length('US-6227309-B1-transform.xml', 'abstract')
testing_length('US-6186162-B1-transform.xml', 'abstract')
testing_length('US-6199245-B1-transform.xml','abstract')
testing_length('US-6208446-B1-transform.xml','abstract')
testing_length('US-6222785-B1-transform.xml','abstract')


def summary_test(file_name):
    root = growTree.grow_tree(file_name)
    # may need to change it to guiding transformation
    fs = FrequencySummarizer.FrequencySummarizer()
    for abstract in root.findall("abstract"):
        entered_text = abstract.text
        for s in fs.summarize(entered_text,1):
            print('*', s)


summary_test('US-6227309-B1-transform.xml')
summary_test('US-6186162-B1-transform.xml')
summary_test('US-6199245-B1-transform.xml')
summary_test('US-6208446-B1-transform.xml')
summary_test('US-6222785-B1-transform.xml')

# def abstracted_files(available_dir):
#      for file_found in [f for f in os.listdir(available_dir) if f.endswith('.xml')]:
#          testing_length(file_found,'abstract')
#          summary_test(file_found)
#          bag_of_words.prepare_answers_from_XML(file_found,'abstract')


#abstracted_files('C:/Users/Tara/PycharmProjects/untitled/transformed_files')

bag_of_words.prepare_answers_from_XML('US-6227309-B1-transform.xml', 'abstract')
bag_of_words.prepare_answers_from_XML('US-6186162-B1-transform.xml', 'abstract')
bag_of_words.prepare_answers_from_XML('US-6199245-B1-transform.xml', 'abstract')
bag_of_words.prepare_answers_from_XML('US-6208446-B1-transform.xml', 'abstract')
bag_of_words.prepare_answers_from_XML('US-6222785-B1-transform.xml', 'abstract')

#for now, this is on the already transformed XML files. I will add the guiding_transformation
#module to account for the new transformed files