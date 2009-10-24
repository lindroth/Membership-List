try:  
        import pygtk  
        pygtk.require("2.0")  
except:  
        pass  
try:  
        import gtk  
except:  
        print("GTK Not Availible")
        sys.exit(1)

from lib.member import Member
from lib.person import Person
import time

class Window:
  """This class is used to show wineDlg"""
	
  def __init__(self, glade_file):
	
    #setup the glade file
		self.gladefile = "gui/member.glade"


  def run(self, person):
    builder = gtk.Builder()
    builder.add_from_file(self.gladefile)

		#Get the actual dialog widget
    self.store_member = builder.get_object("store_member")

		#Get all of the Entry Widgets and set their text
    firstname_entry = builder.get_object("firstname_entry")
    lastname_entry = builder.get_object("lastname_entry")
    email_entry = builder.get_object("email_entry")
    birthdate_entry = builder.get_object("birtdate_entry")
    streetname_entry = builder.get_object("streetname_entry")
    zipcode_entry = builder.get_object("zipcode_entry")
    city_entry = builder.get_object("city_entry")
    cardnumber_entry = builder.get_object("cardnumber_entry")
    gender = builder.get_object("radiobutton_male")
    payed = builder.get_object("checkbutton_payed")
    
    firstname_entry.set_text(person.firstname)
    lastname_entry.set_text(person.lastname)
    email_entry.set_text(person.email)
    birthdate_entry.set_text(str(person.birthdate))
    streetname_entry.set_text(person.streetname)
    zipcode_entry.set_text(person.zipcode)
    city_entry.set_text(person.city)
    cardnumber_entry.set_text(person.cardnumber)

    gender.set_active(person.gender)
    payed.set_active(person.payed)


		#run the dialog and store the response		
    self.result = self.store_member.run()
    
    valid_date = False

    #while not valid_date:
    #  try:
    #    print "check"
    #    time.strptime(birthdate_entry.get_text(), '%Y-%m-%d')
    #    valid_date = True
    #  except ValueError:
    #    birthdate_entry.set_text("Not valid date YYYY-MM-DD")
    #    print "run"
    #    self.result = self.store_member.run()

    person.firstname = firstname_entry.get_text()
    person.lastname = lastname_entry.get_text()
    person.email = email_entry.get_text()
    person.birthdate = birthdate_entry.get_text()
    person.streetname = streetname_entry.get_text()
    person.zipcode = zipcode_entry.get_text()
    person.city = city_entry.get_text()
    person.cardnumber = cardnumber_entry.get_text()
    person.gender = gender.get_active()
    person.payed = payed.get_active()
    person.sample = None

		#we are done with the dialog, destory it
    self.store_member.destroy()
		
		#return the result and the wine
    return self.result,person
