try:
    from sqlobject import *
except:
    print("Sqlobject Not Available")
    sys.exit(1)

class Swipe(SQLObject):
  person = ForeignKey('Person')
  date = DateTimeCol()

