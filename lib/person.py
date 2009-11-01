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
  

  property_names = [
      "id",
      "Firstname", 
      "Lastname",
      "Birtdate",
      "Payed",
      "email",
      "Post Address",
      "City",
      "Cardnumber",
      "Gender",
      ]

  hidden_properties = [
      "id",
      "Cardnumber"
      ]

  def to_array(self):
    if self.gender:
      gender_string = "Male"
    else:
      gender_string = "Female"
  
    return [
        self.id,
        self.firstname, 
        self.lastname, 
        self.birthdate,
        self.payed, 
        self.email,
        self.streetname,
        self.post_address,
        self.cardnumber,
        gender_string
        ]
  #def  _init(self, *args, **kw):
  #  SQLObject._init(self, *args, **kw)
