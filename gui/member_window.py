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

from lib.person import Person
import time
from lib.read_card import Card

class Window:
  """This class is used to show wineDlg"""
	
  def __init__(self, glade_file):
	
    #setup the glade file
    self.gladefile = "gui/member.glade"
 
  def on_associate_new_card(self, widget):
    card = Card(self.reading_card_result, self.on_card_found)
    card.start()

  def on_card_found(self,cardnumber):
    cardnumber_entry = self.builder.get_object("cardnumber_entry")
    cardnumber_entry.set_text(cardnumber)
 
  def reading_card_result(self, foo):
    print "No card found!"

  def run(self, person = None):
    self.builder = gtk.Builder()
    self.builder.add_from_file(self.gladefile)

    signals = { 
        "on_associate_new_card" : self.on_associate_new_card,
    }

    self.builder.connect_signals(signals)
		#Get the actual dialog widget
    self.store_member = self.builder.get_object("store_member")

		#Get all of the Entry Widgets and set their text
    firstname_entry = self.builder.get_object("firstname_entry")
    lastname_entry = self.builder.get_object("lastname_entry")
    email_entry = self.builder.get_object("email_entry")
    birthdate_entry = self.builder.get_object("birtdate_entry")
    streetname_entry = self.builder.get_object("streetname_entry")
    post_address_entry = self.builder.get_object("post_address_entry")
    cardnumber_entry = self.builder.get_object("cardnumber_entry")
    radio_male = self.builder.get_object("radiobutton_male")
    radio_female = self.builder.get_object("radiobutton_female")
    payed = self.builder.get_object("checkbutton_payed")
    
    if(person):
      firstname_entry.set_text(person.firstname)
      lastname_entry.set_text(person.lastname)
      email_entry.set_text(person.email)
      birthdate_entry.set_text(str(person.birthdate))
      streetname_entry.set_text(person.streetname)
      post_address_entry.set_text(person.post_address)
      cardnumber_entry.set_text(person.cardnumber)
     
      print "JASDSADSAD:" + str(person.gender)
      if(person.gender):
        print "Set active M"
        radio_male.set_active(True)
      else:
        print "Set active F"
        radio_female.set_active(False)
      
      if(not person.payed):
        self.store_member.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))
      else:
        self.store_member.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
      payed.set_active(person.payed)
      
      


		#run the dialog.
    self.result = self.store_member.run()
    
    if(person):
      person.firstname = firstname_entry.get_text()
      person.lastname = lastname_entry.get_text()
      person.email = email_entry.get_text()
      person.birthdate = birthdate_entry.get_text()
      person.streetname = streetname_entry.get_text()
      person.post_address = post_address_entry.get_text()
      person.cardnumber = cardnumber_entry.get_text()
      person.gender = radio_male.get_active()
      person.payed = payed.get_active()
      person.sample = None
    else:
      person = Person(
          firstname = firstname_entry.get_text(),
          lastname = lastname_entry.get_text(),
          email = email_entry.get_text(),
          birthdate = birthdate_entry.get_text(),
          streetname = streetname_entry.get_text(),
          post_address = post_address_entry.get_text(),
          cardnumber = cardnumber_entry.get_text(),
          gender = radio_male.get_active(),
          payed = payed.get_active(),
          sample = None
          )

		#we are done with the dialog, destory it
    self.store_member.destroy()
		
		#return the result and the wine
    return self.result,person
