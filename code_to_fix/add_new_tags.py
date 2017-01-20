import growTree
import using_transformed_files

class add_new_tags:
    def __init__(self, file_name, new_tag):
        self.fn = file_name
        self.nt = new_tag

    def insert_tag(self, file_name, new_tag):
        root = growTree.grow_tree(file_name)
        tag1 = root.append(new_tag)
        return root, tag1

    def save_file(self, file_name):
        addition = 'transformadd.xml'
        new_tag1 = "summarized-abstract"
        new_tag2 = "bag-of-words"
        new_tree, tag1 = self.insert_tag(file_name, new_tag1)
        tag1.text = using_transformed_files.testing_length(file_name, 'abstract')
        new_tree, tag2 = self.insert_tag(file_name, new_tag2)
        tag2.text = using_transformed_files.create_bag_of_words(file_name)
        #change the file name



