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

class Window:
  """This class is used to show wineDlg"""
	
  def __init__(self, glade_file):
	
    #setup the glade file
		self.gladefile = "gui/member.glade"
  
  def run(self):
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
    payed_entry = builder.get_object("checkbutton_payed")

		#run the dialog and store the response		
    self.result = self.store_member.run()

    #gender

    #get the value of the entry fields
    new_person = Person(
        firstname = firstname_entry.get_text(),
        lastname = lastname_entry.get_text(),
        email = email_entry.get_text(),
        birthdate = birthdate_entry.get_text(),
        streetname = streetname_entry.get_text(),
        zipcode = zipcode_entry.get_text(),
        city = city_entry.get_text(),
        cardnumber = cardnumber_entry.get_text(),
        gender = gender.get_active(),
        payed = payed_entry.get_active(),
        sample = None
        )

		#we are done with the dialog, destory it
    self.store_member.destroy()
		
		#return the result and the wine
    return self.result,new_person
