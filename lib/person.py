from sqlobject import *
path = "/home/gny/Develop/eatingbits/membership_list/db/"
sqlhub.processConnection = connectionForURI('sqlite:///'+ path +'new.db')

class Person(SQLObject):
  firstname = StringCol()
  lastname = StringCol()
  cardnumber = StringCol()
  payed = BoolCol()
  gender = BoolCol()
  birthdate = StringCol()
  streetname = StringCol()
  zipcode = StringCol()
  city = StringCol()
  email = StringCol()
  sample = StringCol() 
  
  #def  _init(self, *args, **kw):
  #  SQLObject._init(self, *args, **kw)
