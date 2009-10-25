from sqlobject import *
import os

path =  os.path.abspath(".") + "/db/"
sqlhub.processConnection = connectionForURI('sqlite:///'+ path +'new.db')

class Person(SQLObject):
  firstname = StringCol()
  lastname = StringCol()
  cardnumber = StringCol()
  payed = BoolCol()
  gender = BoolCol()
  birthdate = StringCol()
  streetname = StringCol()
  post_address = StringCol()
  email = StringCol()
  sample = StringCol() 
  
  #def  _init(self, *args, **kw):
  #  SQLObject._init(self, *args, **kw)
