import sys

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
import datetime

class Window:
    def __init__(self, glade_file):
        gladefile = "gui/member.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)

    def on_associate_new_card(self, widget):
        card = Card(self.reading_card_result, self.on_card_found)
        card.start()

    def on_card_found(self,cardnumber):
        cardnumber_entry = self.builder.get_object("cardnumber_entry")
        cardnumber_entry.set_text(cardnumber)

    def on_manual_swipe(self, widget):
      if(self.person):
        self.person.add_date()
      print "Added date to person" 


    def reading_card_result(self, foo):
        print "No card found!"

    def run(self, person = None):
        self.person = person

        signals = {
            "on_associate_new_card" : self.on_associate_new_card,
            "on_manual_swipe" : self.on_manual_swipe,
        }

        self.builder.connect_signals(signals)
        self.store_member = self.builder.get_object("store_member")

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

        if(self.person):
            #This is an edit, set the fields
            firstname_entry.set_text(self.person.firstname)
            lastname_entry.set_text(self.person.lastname)
            email_entry.set_text(self.person.email)
            birthdate_entry.set_text(str(self.person.birthdate))
            streetname_entry.set_text(self.person.streetname)
            post_address_entry.set_text(self.person.post_address)
            cardnumber_entry.set_text(self.person.cardnumber)

            if(self.person.gender):
                print "Set active M"
                radio_male.set_active(True)
            else:
                print "Set active F"
                radio_female.set_active(False)

            if(not self.person.payed):
                self.store_member.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))
            else:
                self.store_member.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
            payed.set_active(self.person.payed)


        self.result = self.store_member.run()

        if(self.result == gtk.RESPONSE_OK):
            #If this is on add and not edit we need to create a person
            if(not self.person):
                self.person = Person()

            self.person.firstname = firstname_entry.get_text()
            self.person.lastname = lastname_entry.get_text()
            self.person.email = email_entry.get_text()
            self.person.birthdate = birthdate_entry.get_text()
            self.person.streetname = streetname_entry.get_text()
            self.person.post_address = post_address_entry.get_text()
            self.person.cardnumber = cardnumber_entry.get_text()
            self.person.gender = radio_male.get_active()
            self.person.payed = payed.get_active()
            self.person.sample = None

        self.store_member.destroy()

        return self.result,self.person
