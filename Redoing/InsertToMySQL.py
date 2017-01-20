# -*- coding: utf-8 -*-
import peewee as pw
# import mysql.connector  # For InsertWithSQL
import pymysql
from lxml import etree
from datetime import datetime
import os
import codecs
import random



from models import *



def InsertWithSQL():
    mySQLConnection = mysql.connector.connect(user='olegscom_moto', password='Motopatent1',
                                              host='50.116.69.17',
                                              database='olegscom_moto01')

    cursor = mySQLConnection.cursor()

    try:
        ucid = '12456'
        cursor.execute("""INSERT INTO `NLCTrainGNoDupesNLCtrain-db` (Abstract, Class)  VALUES (%s,%s)""", (ucid, ucid))
        mySQLConnection.commit()
        print "Inserted " + ucid
    except Exception, e:
        print "InsertIntoMySQL: " + str(e)
        mySQLConnection.rollback()

    mySQLConnection.close()

def ConnectWithORM():

    myDB = pw.MySQLDatabase("olegscom_moto01", host="50.116.69.17", port=3306, user="olegscom_moto",
                            passwd="Motopatent1")

    class Abstract(pw.Model):
        """A base model that will use our MySQL database"""
        Abstract = pw.CharField()
        Class = pw.CharField()
        ID = pw.CharField()

        class Meta:
            database = myDB
            db_table = 'NLCTrainGNoDupesNLCtrain-db'



    # when you're ready to start querying, remember to connect
    myDB.connect()


    print Abstract.select().where(Abstract.ID=="5").get().Abstract


    myDB.close()

def InsertRows():
    #Patent.create_table()  # then: alter table patents convert to character set utf8mb4 collate utf8mb4_unicode_ci;

    ucids = ["12314", "45567", "58659", "i8687t"]
    #for ucid in ucids:
     #   patent, created = Patent.get_or_create(ucid=ucid)
    #    patent.docType = "test3"
    #    patent.save()




def GetOrInsertDirOfTransformedXMLIntoDB():

    sourceBaseDir = 'C:/Users/Tara/PyCharmProjects/untitled/sourceNLCNoDupes/'
    dirsWithXML = [
                   'ipa150205',
                   'ipa150212',
                   'ipa150219',
                   'ipa150226',
                   'ipa150305',
                   'ipa150312',
                   'ipa150319',
                   'ipa150326',
                   'ipa150402',
                   'ipa150409',
                   'ipa150416',
                   'ipa150423',
                   'ipa150430',
                   'ipa150507',
                   'ipa150514',
                   'ipa150521',
                   'ipa150528',
                   'ipa150604',
                   'ipa150611',
                   'ipa150618',
                   'ipa150625',
                   'ipa150702',
                   'ipa150709',
                   'ipa150716',
                   'ipa150723',
                   'ipa150730',
                   'ipa150806',
                   'ipa150813',
                   'ipa150820',
                   'ipa150827',
                   'ipa150903',
                   'ipa150910',
                   'ipa150917',
                   'ipa150924',
                   'ipa151001',
                   'ipa151008',
                   'ipa151015',
                   'ipa151022',
                   'ipa151029',
                   'ipa151105',
                   'ipa151112',
                   'ipa151119',
                   'ipa151126',
                   'ipa151203',
                   'ipa151210',
                   'ipa151217',
                   'ipa151224',
                   'ipa151231',
                   'ipa160107',
                   'ipa160114',
                   'ipa160121',
                   'ipa160128',
                   'ipa160204',
                   'ipa160211',
                   'ipa160218',
                   'ipa160225',
                   'ipa160303',
                   'ipa160310',
                   'ipa160317',
                   'ipa160324',
                   'ipa160331',
                   'ipa160407',
                   'ipa160414',
                   'ipa160421',
                   'ipa160428',
                   'ipa160505',
                   'ipa160512',
                   'ipa160519',
                   'ipa160526',
                   'ipa160602',
                   'ipa160609',
                   'ipa160616',
                   'ipa160623',
                   'ipa160630',
                   'ipa160707',
                   'ipa160714',
                   'ipa160721',
                   'ipa160728',
                   'ipa160804',
                   'ipa160811',
                   'ipa160818',
                   'ipa160825',
                   'ipa160901',
                   'ipa160908',
                   'ipa160915',
                   'ipa160922',
                   'ipa160929',
                   'ipa161006',
                   'ipa161013',
                   'ipa161020',
                   'ipa161027',
                   'ipa161103']
    for dirWithXML in dirsWithXML:
        baseDir = sourceBaseDir + dirWithXML
        print "Working on " + baseDir + " now."
        os.chdir(baseDir)
        # For each transformed xml file in source directory
        for transXMLFile in [f for f in os.listdir(baseDir) if f.endswith('xml')]:
            try:
                parsed_xml = etree.parse(codecs.open(transXMLFile, encoding='utf-8'))

                patentInfo = parsed_xml.getroot().find('patent-info')

                #elemList = []

                ucid = patentInfo.find('Patent').text
                pwPatent, created = Patent.get_or_create(Patent=ucid)

                for elem in list(patentInfo):
                    #elemList.append(elem.tag)
                    #print patentInfo.find(elem.tag).text
                    # http://stackoverflow.com/questions/2612610/how-to-access-object-attribute-given-string-corresponding-to-name-of-that-attrib
                    setattr(pwPatent, elem.tag, patentInfo.find(elem.tag).text)


                #print elemList
                # http://stackoverflow.com/questions/29596584/getting-a-list-of-xml-tags-in-file-using-xml-etree-elementtree

                pwPatent.save()

                print ucid + " created: " + str(created)

                # Should move to Python 3????
                # http://stackoverflow.com/questions/37899889/sqlalchemy-reports-invalid-utf8mb4-character-string-for-binary-column

            except Exception, e:
                print "InsertDirOfTransformedXMLIntoDB: " + str(e)
                pass

def BulkInsertDirOfTransformedXMLIntoDB():
    # PatentClean.drop_table()
    # PatentClean.create_table()
    dirsWithXML = [

                   'ipa150205',
                   'ipa150212',
                   'ipa150219',
                   'ipa150226',
                   'ipa150305',
                   'ipa150312',
                   'ipa150319',
                   'ipa150326',
                   'ipa150402',
                   'ipa150409',
                   'ipa150416',
                   'ipa150423',
                   'ipa150430',
                   'ipa150507',
                   'ipa150514',
                   'ipa150521',
                   'ipa150528',
                   'ipa150604',
                   'ipa150611',
                   'ipa150618',
                   'ipa150625',
                   'ipa150702',
                   'ipa150709',
                   'ipa150716',
                   'ipa150723',
                   'ipa150730',
                   'ipa150806',
                   'ipa150813',
                   'ipa150820',
                   'ipa150827',
                   'ipa150903',
                   'ipa150910',
                   'ipa150917',
                   'ipa150924',
                   'ipa151001',
                   'ipa151008',
                   'ipa151015',
                   'ipa151022',
                   'ipa151029',
                   'ipa151105',
                   'ipa151112',
                   'ipa151119',
                   'ipa151126',
                   'ipa151203',
                   'ipa151210',
                   'ipa151217',
                   'ipa151224',
                   'ipa151231',
                   'ipa160107',
                   'ipa160114',
                   'ipa160121',
                   'ipa160128',
                   'ipa160204',
                   'ipa160211',
                   'ipa160218',
                   'ipa160225',
                   'ipa160303',
                   'ipa160310',
                   'ipa160317',
                   'ipa160324',
                   'ipa160331',
                   'ipa160407',
                   'ipa160414',
                   'ipa160421',
                   'ipa160428',
                   'ipa160505',
                   'ipa160512',
                   'ipa160519',
                   'ipa160526',
                   'ipa160602',
                   'ipa160609',
                   'ipa160616',
                   'ipa160623',
                   'ipa160630',
                   'ipa160707',
                   'ipa160714',
                   'ipa160721',
                   'ipa160728',
                   'ipa160804',
                   'ipa160811',
                   'ipa160818',
                   'ipa160825',
                   'ipa160901',
                   'ipa160908',
                   'ipa160915',
                   'ipa160922',
                   'ipa160929',
                   'ipa161006',
                   'ipa161013',
                   'ipa161020',
                   'ipa161027',
                   'ipa161103']

    #dirsWithXML = ['ipa160407', 'ipa160811', 'ipa160818', 'ipa160825', 'ipa160901', 'ipg160726', 'ipg160802', 'ipg160809', 'ipg160816', 'ipg160830']  # Is both source and target final directory name
    #dirsWithXML = ['ipg160726']
    sourceBaseDir = 'C:/Users/Tara/PyCharmProjects/untitled/sourceNLCNoDupes/'
    PatentsInserted = 0

    for dirWithXML in dirsWithXML:
        baseDir = sourceBaseDir + dirWithXML
        print "Working on " + baseDir + " now."
        os.chdir(baseDir)

        print "xml files in directory: " + str(len([name for name in os.listdir(baseDir) if os.path.isfile(os.path.join(baseDir, name))]))
        # For each transformed xml file in source directory

        #create list to hold dicionaries of patents for bulk insert
        ValidPatentsInDir = []



        for transXMLFile in [f for f in os.listdir(baseDir) if f.endswith('xml')]:
            try:
                parsed_xml = etree.parse(codecs.open(transXMLFile, encoding='utf-8'))
                patentInfo = parsed_xml.getroot().find('patent-info')

                singlePatent = {}  # dictionary for individual patents

                #Set dictionary to have all fields from Model (and empty) so bulk insert works
                for patentField in PatentClean._meta.fields.keys():
                    singlePatent.update({patentField: None})

                #print "elements in dict: " + str(len(singlePatent))
                #print singlePatent

                #ucid = patentInfo.find('ucid').text

                for elem in list(patentInfo):
                    elementText = patentInfo.find(elem.tag).text
                    if elementText and elementText.strip():
                        elementText = ' '.join(elementText.split())  # remove extra whitespace
                        singlePatent.update({elem.tag: elementText})

                #Add single patent dictionary to list of dictionaries
                #skip/remove plants and reissues, design, dna sequences here
                if not (singlePatent['Patent'].startswith(("PP", "RE", "D")) or singlePatent['Patent'].endswith(("SEQ"))):

                    # Prep data which can't be handled by the xsl transform
                    if singlePatent['NationalUSFieldSearch'] == "Non/e":
                        singlePatent['NationalUSFieldSearch'] = None

                    if singlePatent['CPCfurther'] and len(singlePatent['CPCfurther']) == 4:
                        singlePatent['CPCfurther'] = None
                    elif singlePatent['CPCfurther'] and len(singlePatent['CPCfurther']) > 4:
                        singlePatent['CPCfurther'] = singlePatent['CPCfurther'][6:]

                    singlePatent['Random'] = random.random()

                    del singlePatent['ClaimAll']

                    ValidPatentsInDir.append(singlePatent)
                    print singlePatent['Patent']
                else:
                    print singlePatent['Patent'] + " skipped"


                # Should move to Python 3????
                # utf8 decoder: https://software.hixie.ch/utilities/cgi/unicode-decoder/utf8-decoder
                # Funny chars in: 09407339.xml dir: ipg160802
                # http://stackoverflow.com/questions/37899889/sqlalchemy-reports-invalid-utf8mb4-character-string-for-binary-column

            except Exception, e:
                print "InsertDirOfTransformedXMLIntoDB: " + str(e)
                pass

        print "Inserting from: " + baseDir

        # http://docs.peewee-orm.com/en/latest/peewee/querying.html
        with myDB.atomic():
            batchSize = 1000
            totalInDir = len(ValidPatentsInDir)
            for idx in range(0, totalInDir, batchSize):
                print "inserted batch of " + str(batchSize) + ", total: " + str(idx) + " of " + str(totalInDir)
                PatentClean.insert_many(ValidPatentsInDir[idx:idx + batchSize]).execute()
                #print "inserted batch of " + str(batchSize) + ", total: " + str(idx) + " of " + str(totalInDir)

            PatentsInserted += totalInDir
            print "Inserted many: " + str(PatentsInserted)

# InsertWithSQL()
# InsertWithORM()
#InsertRows()
#GetInsertDirOfTransformedXMLIntoDB()

startTime = datetime.now()
print "Start time: " + str(startTime)
BulkInsertDirOfTransformedXMLIntoDB()
endTime = datetime.now()
print "End time: " + str(endTime)
print "Total time(s): " + str((endTime-startTime).total_seconds())











