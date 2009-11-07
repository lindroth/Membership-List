from sqlobject import *

class Swipe(SQLObject):
  person = ForeignKey('Person')
  date = DateTimeCol()

