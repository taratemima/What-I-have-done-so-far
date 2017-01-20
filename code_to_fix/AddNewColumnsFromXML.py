from code_to_fix import FrequencySummarizer


class AddNewColumnsFromXML:
    def __init__(self, xml_file, xsl_file, search_term):
        self.xml = xml_file
        self.xsl = xsl_file
        self.st = search_term
        self.new_tags = []

    def add_new_tag(self, tag):
        self.new_tags.append(tag)

    def output_check(self, transform_tree, search_term):
        for element in transform_tree:
            for found in element.findall(search_term):
                if found.count(' ') < 1000:
                    self.add_new_tag('summarized-text')
                    self.add_new_tag('extracted-keywords')
                    clean_text = normalize(found)
                    available_words = bag_of_words.create_bag_of_words(clean_text)
                    return clean_text, available_words
                else:
                    self.add_new_tag('extracted-keywords')
                    clean_text = normalize(found)
                    fs = FrequencySummarizer.FrequencySummarizer()
                    short_text = fs.summarize(clean_text, 1)
                    available_words = bag_of_words.create_bag_of_words(clean_text)
                    return short_text, available_words


firstFileFirstSearch = AddNewColumnsFromXML('US-6186162-B1.xml', 'new_patents.xsl', 'abstract')
firstFileSecondSearch = AddNewColumnsFromXML('US-6186162-B1.xml', 'new_patents.xsl', 'claim')
secondFileFirstSearch = AddNewColumnsFromXML('US-20150125472-A1.xml', 'new_patents.xsl', 'abstract')
secondFileSecondSearch = AddNewColumnsFromXML('US-20150125472-A1.xml', 'new_patents.xsl', 'claim')

print firstFileFirstSearch.new_tags
print firstFileSecondSearch.new_tags
print secondFileFirstSearch.new_tags
print secondFileSecondSearch.new_tags
