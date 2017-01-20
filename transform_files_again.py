from lxml import etree
import os


# target_folder: C:\Users\Tara\PyCharmProjects\untitled\transformed_files\
# source_folder: C:\Users\Tara\PyCharmProjects\untitled\toBeTransformed

def transform_file(xml_file, xsl_file):
    parsed_xsl = etree.parse(xsl_file)
    parsed_xml = etree.parse(xml_file)
    transform = etree.XSLT(parsed_xsl)
    return transform(parsed_xml)


def create_new_file_name(xml_file):
    original = os.path.splitext(xml_file)
    return str(original[0] + "transform.xml")


def write_complete_file(new_file_name, transformed_tree):
    outfile = open(os.path.join('C:/Users/Tara/PyCharmProjects/untitled/toBeTransformed/transformed_files/', new_file_name), 'w')
    transformed_tree.write(outfile)


def test_for_transformed_file(source_file):
    transformed = transform_file(source_file, 'C:/Users/Tara/PyCharmProjects/untitled/toBeTransformed/new_patents.xsl')
    new_fn = create_new_file_name(source_file)
    write_complete_file(new_fn, transformed)
    # available_files = [os.listdir(target_folder)]
    # new_fn = create_new_file_name(source_file)
    # if new_fn in available_files:
    #     print "File already exists."
    # else:

    #     newf = create_new_file_name(source_file)
    #     os.chdir(target_folder)
    #     write_complete_file(newf, transformed, target_folder)
    # http: // stackoverflow.com / questions / 8024248 / telling - python - to - save - a - txt - file - to - a - certain - directory - on - windows - and -mac


def transform_and_write():
    for s in [f for f in os.listdir("C:/Users/Tara/PyCharmProjects/untitled/toBeTransformed/") if f.endswith('.xml')]:
        os.chdir("C:/Users/Tara/PyCharmProjects/untitled/toBeTransformed/")
        test_for_transformed_file(s)
#     """
#
#     :param source:
#     :param target:
#     """

#     while source_list[1:10]:
#         i = iter(source_list)
#         os.chdir(source)
#         file_found = i.next()
#         try:
#             transformed = transform_file(file_found, 'new_patents.xsl')
#             newf = create_new_file_name(file_found)
#             os.chdir(os.pardir)
#             os.chdir(target)
#             write_complete_file(newf, transformed)
#         except IOError:
#             i.next()



transform_and_write()

# got an error message because of the first file, how do I go on to the next file in list?