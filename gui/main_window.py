# This Python file uses the following encoding: utf-8
import sys

try:  
        import pygtk  
        pygtk.require("2.0")  
except:  
        pass  
try:  
        import gtk
        import gobject
except:  
        print("GTK Not Availible")
        sys.exit(1)

#import store_member
#import edit_member
import member_window

from lib import rfid
from lib.person import Person
from lib.read_card import Card
from sqlobject import AND

import time

gtk.gdk.threads_init()

class Window:

  def __init__(self, glade_file):
    
    self.readingcard = False
    self.card = Card(self.reading_card_result, self.on_card_found)

    self.glade_file = glade_file
    member_properties = [
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
  
    self.builder = gtk.Builder()
    self.builder.add_from_file(glade_file)

    signals = { 
        "quit" : self.quit,
        "on_buttonQuit_clicked" : self.quit,
        "on_window_destroy" : self.quit,
        "on_add_member" : self.on_add_member,
        "on_edit_member" : self.on_edit_member,
        "on_start_stop_rfid_reader" : self.on_start_stop_rfid_reader,
        "on_find" : self.on_search_button,
        "on_delete_member" : self.on_delete_member,
        "on_card_found" : self.on_card_found,
        "on_clear_search" : self.on_clear_search,
        "on_row_activated" : self.on_edit_member,
    }
    self.builder.connect_signals(signals)

    self.member_tree_view = self.builder.get_object("memberview")

    self.add_columns_to_tree_view(self.member_tree_view, member_properties)
	
    self.member_list = gtk.ListStore(str, str, str, str, str, str,
        str, str, str, str )
    self.member_tree_view.set_model(self.member_list)	

    #Set up db connection.
    Person.createTable(ifNotExists=True)
    
    self.show_all_members()

    self.main_window = self.builder.get_object("main_window")
    self.main_window.show()
    gtk.main()


  def show_all_members(self):
    members = Person.select()
    self.show_members(members)


  def show_members(self, members):
    self.member_list.clear()
    for member in members:
      self.member_list.append(self.member_to_array(member) )


  def member_to_array(self, member):
    if member.gender:
      gender_string = "Male"
    else:
      gender_string = "Female"

    return [
        member.id,
        member.firstname, 
        member.lastname, 
        member.birthdate,
        member.payed, 
        member.email,
        member.streetname,
        member.post_address,
        member.cardnumber,
        gender_string
        ]


  def add_columns_to_tree_view(self, list_store, member_properties):
    """Add all of the List Columns to the member_tree_view"""
    column_number = 0
    for column_name in member_properties:
      self.add_column(list_store, column_name, column_number)
      column_number += 1


  def add_column(self,list_store, title, column_number):
    """This function adds a column to the list view.
    First it create the gtk.TreeViewColumn and then set
    some needed properties"""
						
    column = gtk.TreeViewColumn(title, gtk.CellRendererText()
      , text=column_number)
    column.set_resizable(True)		
    column.set_sort_column_id(column_number)
    if(title == "id" or title == "Cardnumber"):
      column.set_visible(False)
    list_store.append_column(column)


  def on_search_button(self, widget):
    firstname = self.builder.get_object("firstname_search_entry").get_text()
    lastname = self.builder.get_object("lastname_search_entry").get_text()
    members = Person.select(AND(Person.q.firstname.startswith(firstname),
      Person.q.lastname.startswith(lastname)))
    self.show_members(members)


  def on_window_destroy(self, widget, data=None ):
    gtk.main_quit()

  
  def on_delete_member(self, widget):
    pass
    #selection = self.member_tree_view.get_selection()
    #model, path = selection.get_selected()

    #if path:
    #  person_id = model[path][0]
    #  self.member_list.remove(path)
    #  Person.delete(person_id)
    

  def on_clear_search(self, widget):
    self.builder.get_object("firstname_search_entry").set_text("")
    self.builder.get_object("lastname_search_entry").set_text("")
    self.show_all_members()

  def on_add_member(self, widget):
    #Cteate the dialog, show it, and store the results
    self.card.stop()
		
    add_member_dialog = member_window.Window(self.glade_file)
    result,new_member = add_member_dialog.run()

    if (result == gtk.RESPONSE_OK):
      #	"""The user clicked Ok, so let's add this
      #	member to the member list"""
      self.member_list.append(self.member_to_array(new_member))
    else:
      Person.delete(new_member.id)

    if(self.readingcard):
      self.card.start()


  def reading_card_result(self, input):
    label = self.builder.get_object("reading_card_label")
    if(label.get_label() == "reading"):
      label.set_label("")
    else:
      label.set_label("reading")
    print input


  def on_card_found(self, cardnumber):
    #self.card.stop()
    person_found = Person.select(Person.q.cardnumber == cardnumber)
    person_list = list(person_found)
    if len(person_list):
      print "Member found :" + str(person_list[0].id)
      import pprint
      gobject.idle_add(self.start_edit_dialoge,person_list[0])
    else:
      print "No Member with cardnumber : " + cardnumber


  def on_start_stop_rfid_reader(self,widget):

    label = self.builder.get_object("reading_card_label")
    statusbar = self.builder.get_object("statusbar")

    #test to start thread
    button = self.builder.get_object("start_stop_button")
    if not self.readingcard:
      statusbar.push(1,"reading")
      print "Start"
      label.set_label("")
      button.set_label("Stop RFID reader")
      self.readingcard = True
      self.card.start()
    else:
      statusbar.pop(1)
      label.set_label("reading")
      print "Stop"
      button.set_label("Start RFID reader")
      self.card.stop()
      self.readingcard = False

  
  def start_edit_dialoge(self, person_to_edit, place_in_tree_view = None):
    self.card.stop()
    edit_member_dialog = member_window.Window(self.glade_file)
    result,new_member = edit_member_dialog.run(person_to_edit)

    if (result == gtk.RESPONSE_OK):
      #	The user clicked Ok, So I guess we should find the member and remove 
      #him from the search list
      print "Back"
      if(place_in_tree_view):
        self.member_list.remove(place_in_tree_view)
        self.member_list.append(self.member_to_array(new_member))
    if(self.readingcard):
      self.card.start()
      
    gtk.main()

  def on_edit_member(self, widget, path = None, view_column = None):
    selection = self.member_tree_view.get_selection()
    model, path = selection.get_selected()

    if path:
      person_to_edit = Person.get(model[path][0])
      self.start_edit_dialoge(person_to_edit, path)


  def quit(self, widget):
    gtk.main_quit
    sys.exit(0)

if __name__ == "__main__":
  app = Member()
  gtk.main()
    
