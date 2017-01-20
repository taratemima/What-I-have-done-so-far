import peewee

# http://www.blog.pythonlibrary.org/2014/07/17/an-intro-to-peewee-another-python-orm/
# https://teamtreehouse.com/community/unicode-issues-while-using-peewee-pymysql-and-python
myDB = peewee.MySQLDatabase("olegscom_moto01", host="50.116.69.17", port=3306, user="olegscom_moto",
                            passwd="Motopatent1", charset='utf8mb4')

class BaseModel(peewee.Model):
    class Meta:
        database = myDB

class Patent(BaseModel):
    """A base model that will use our MySQL database"""
    ucid = peewee.CharField(max_length=100, primary_key=True, unique=True)
    docType = peewee.TextField(null=True)
    country = peewee.TextField(null=True)
    patentType = peewee.TextField(null=True)
    company = peewee.TextField(null=True)
    assignee = peewee.TextField(null=True)
    applicationDate = peewee.DateTimeField(null=True)
    publicationDate = peewee.DateTimeField(null=True)
    ipcrAll = peewee.TextField(null=True)
    cpcMain = peewee.TextField(null=True)
    cpcMainSection = peewee.TextField(null=True)
    cpcMainClass = peewee.TextField(null=True)
    cpcMainSubclass = peewee.TextField(null=True)
    cpcMainClassSubclass = peewee.TextField(null=True)
    cpcFurther = peewee.TextField(null=True)
    cpcFurtherCSVNoDupes = peewee.TextField(null=True)
    cpcMainFirstPlusFurtherCSVNoDupes = peewee.TextField(null=True)
    usSearchClasses1stFull = peewee.TextField(null=True)
    usSearchClassesAll = peewee.TextField(null=True)
    usSearchClasses1st1st3Chars = peewee.TextField(null=True)
    usSearchClassesAllSlashes = peewee.TextField(null=True)
    usSearchClassesAll1st3Chars = peewee.TextField(null=True)
    cpcSearchClassesAll = peewee.TextField(null=True)
    cpcSearchClasses1st4Chars = peewee.TextField(null=True)
    title = peewee.TextField(null=True)
    abstract = peewee.TextField(null=True)
    claim1Text = peewee.TextField(null=True)
    allClaimsText = peewee.TextField(null=True)

    class Meta:
        db_table = 'patents_temp'

    # https://github.com/coleifer/peewee/issues/673
    #@classmethod
    #def create_table(cls, fail_silently=False):
        #super(Patent, cls).create_table(fail_silently=fail_silently)
        #cls._meta.database.execute_sql('CREATE INDEX patents_ucid ON patents (ucid(255))')


class PatentClean(BaseModel):
    """A base model that will use our MySQL database"""
    Patent = peewee.CharField(max_length=100, primary_key=True, unique=True)
    Status = peewee.TextField(null=True)
    Country = peewee.TextField(null=True)
    Type = peewee.TextField(null=True)
    Company = peewee.TextField(null=True)
    Assignee = peewee.TextField(null=True)
    ApplicationDate = peewee.DateTimeField(null=True)
    PublicationDate = peewee.DateTimeField(null=True)
    IPCall = peewee.TextField(null=True)
    CPCmain = peewee.TextField(null=True)
    CPCfurther = peewee.TextField(null=True)
    NationalUSFieldSearch = peewee.TextField(null=True)
    CPCUSFieldSearch = peewee.TextField(null=True)
    Title = peewee.TextField(null=True)
    Abstract = peewee.TextField(null=True)
    Claim1 = peewee.TextField(null=True)
    #ClaimAll = peewee.TextField(null=True)
    Random = peewee.DoubleField(null=True)


    class Meta:
        db_table = 'patents_clean'



if __name__ == "__main__":
    try:
        Patent.create_table()
    except peewee.OperationalError:
        print "Patents table already exists!"
