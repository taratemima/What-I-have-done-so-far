from lxml import etree
import os
import errno
import codecs
# import re
# from HTMLParser import HTMLParser

"""
This actually removes the need to delete a <!DOCTYPE us-patent-grant SYSTEM "us-patent-grant-v45-2014-04-03.dtd" [ ]>
line from each xml file.

:return:
"""

# todo :  Need to check if the resulting xml files, without the root <xml> tag are valid... seem to be as far as Python is concerned

# xslFilePath = 'C:/Users/Oleg/Google Drive/moto/patentsReedTech.xsl'
xslFilePath = 'C:/Users/Tara/PycharmProjects/untitled/patentsReedTech.xsl'
# dirWithXML = 'ipg160830'  # Is both source and target final directory name
# sourceBaseDir = 'C:/bulk-data-tools/bin/'
sourceBaseDir = 'C:/Users/Tara/Documents/Github/bulk-data-tools/bin/'
# targetBaseDir = 'C:/Users/Tara/PyCharmProjects/untitled/moreToTransform/sourceNLCNoDupes/'
targetBaseDir = 'C:/Users/Tara/PycharmProjects/untitled/sourceNLCNoDupes/'
# baseDir = sourceBaseDir + dirWithXML + '/'
# directory with transformed xml file directories

dirsWithXML = ['test']


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def transform_and_rename(dirWithXML):
    baseDir = sourceBaseDir + dirWithXML + '/'  # directory with transformed xml file directories
    # html = HTMLParser()

    os.chdir(baseDir)
    # For each original xml file in source directory
    for origXMLFile in [f for f in os.listdir(baseDir) if f.endswith('xml')]:
        try:
            #  Transform each xml file with the xsl file
            parsed_xsl = etree.parse(codecs.open(xslFilePath, encoding='utf-8'))
            parsed_xml = etree.parse(codecs.open(origXMLFile, encoding='utf-8'))

            transform = etree.XSLT(parsed_xsl)
            result_xml = transform(parsed_xml)

            # for abstract in result_xml.xpath("/reed-patents/patent-info/abstract"):
                # abstract.text = "bob"
                # claim1Text
                # test = re.sub('&#(\d+);', lambda m: chr(int(m.group(1))).decode('cp1252'), abstract.text)
                # abstract.text = re.sub('&#(\d+);', lambda m: chr(int(m.group(1))).decode('cp1252'), abstract.text)

            # result_xml.xpath("/reed-patents/patent-info/abstract")[0].text = html.unescape(result_xml.xpath("/reed-patents/patent-info/abstract")[0].text)

            # result_xml.xpath("/reed-patents/patent-info/allClaimsText")[0].text = \
                #(result_xml.xpath("/reed-patents/patent-info/allClaimsText")[0].text).replace('&lt;', '<')

            # Create target directory if it doesn't exist
            make_sure_path_exists(targetBaseDir + dirWithXML)

            # Start looking through the new xml tree containing the transformed patent info
            for patent in result_xml.iter('patent-info'):
                try:
                    ucid = patent.find('ucid').text  # Find the UCID, we'll use this as our file name
                    print ucid

                    # print patent.find('allClaimsText').text
                    # Look at ucid: 20160234824, in ipa20160811
                    #  Write and/or overwrite
                    outfile = open(os.path.join(targetBaseDir, dirWithXML + '/' + ucid + '.xml'), 'w')
                    result_xml.write(outfile, pretty_print=True, encoding='utf8')
                except Exception, e:
                    print "findUCID: " + str(e)
                    pass
            # print(etree.tostring(result_xml, pretty_print=True))


        except Exception, e:
            print "transform_and_rename: " + str(e)
            pass


def transform_multiple_folders():
    folderNames = ['ipa160407', 'ipa160811', 'ipa160818', 'ipa160825', 'ipa160901', 'ipg160726', 'ipg160802', 'ipg160809', 'ipg160816', 'ipg160830', 'ipg160913', 'ipg160920']
    for f in folderNames:
        transform_and_rename(f)
        # Is both source and target final directory name

# transform_and_rename()
transform_multiple_folders()


