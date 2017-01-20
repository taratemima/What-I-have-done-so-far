# -*- coding: utf-8 -*-
import peewee as pw
import arff


from models import *

 # For timeouts, try this later: http://stackoverflow.com/questions/14726789/how-can-i-change-the-default-mysql-connection-timeout-when-connecting-through-py
try:
    patentsToRequest = 100000
    myPatents = PatentClean.select(PatentClean.CPCmain,
                                   PatentClean.CPCfurther).limit(patentsToRequest)

    count = 0

    print "Requesting " + str(patentsToRequest) + " records."

    Classes_dataset = {
        'description': 'CPC Classes',
        'relation': 'Classes',
        'attributes': [
            ('ClassMain', 'STRING'),
            ('ClassFurther', 'STRING'),
        ],
        'data': [
            ['F01N', 'F02D'],
            ['F01N', 'F02B'],
            ['F01N', 'Y02T'],
            ['F01N', 'B01D']
        ]
    }

    Classes_dataset['data'][:] = []
    ClassMainList = []
    ClassFurtherList = []



    for p in myPatents:
        if p.CPCmain and p.CPCfurther:
            #print "main: " + p.CPCmain + ", Fur:" + p.CPCfurther
            count = count + 1
            for cpcFurtherClass in [x.strip() for x in p.CPCfurther.split(',')]:
                Classes_dataset['data'].append([p.CPCmain, cpcFurtherClass])
                ClassFurtherList.append(cpcFurtherClass)
                ClassMainList.append(p.CPCmain)
                print "main: " + p.CPCmain + ", Fur:" + cpcFurtherClass

    print "Received " + str(count) + " records with a CPC Main and Further class."

    Classes_dataset['attributes'] = [
            ('ClassMain', list(set(ClassMainList))),
            ('ClassFurther', list(set(ClassFurtherList)))]

    # http://stackoverflow.com/questions/25916731/how-to-write-in-arff-file-using-liac-arff-package-in-python
    f = open('trainarff.arff', 'wb')
    arff.dump(Classes_dataset, f)
    f.close()

    print "bob: " + str(Classes_dataset['data'])
except Exception, e:
    print "makeARFF: " + str(e)
    pass




