# This Python file uses the following encoding: utf-8
import datetime
import sys

try:
    import pygtk
    pygtk.require("2.4")
except:
    pass
try:
    import gtk
    import gobject
except:
    print("GTK Not Availible")
    sys.exit(1)

import member_window

from lib.person import Person
from lib.read_card import Card
from sqlobject import AND

import os
import time

gobject.threads_init()

class Window:

    def __init__(self, glade_file):

        db_dir = "db"
        Person.init_db(db_dir)

        try:
            self.card = Card(self.reading_card_result, self.on_card_found)
        except:
            print "No reader found"
            dialog = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_WARNING,
                                   gtk.BUTTONS_OK,
                                   "No RFID reader found")
            result = dialog.run()
            dialog.destroy()
            self.card = None

        self.glade_file = glade_file
        self.blink = False

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
            "on_changed" : self.on_search_button,
        }
        self.builder.connect_signals(signals)

        self.member_tree_view = self.builder.get_object("memberview")
        self.member_tree_view.set_rules_hint(True)

        self.add_columns_to_tree_view(self.member_tree_view, Person)

        # The * is used to expand the tuple in to arguments for the function.
        self.member_list = gtk.ListStore(*Person.get_column_types())
        self.member_tree_view.set_model(self.member_list)

        #Class variables
        self.statusbar = self.builder.get_object("statusbar")
        self.main_window = self.builder.get_object("main_window")

        self.show_all_members()

        #Last words, start state. ugly and for the love of god remove this
        self.card.start()
        button = self.builder.get_object("start_stop_button")
        image = gtk.image_new_from_icon_name("gtk-media-stop", gtk.ICON_SIZE_BUTTON)
        image.show()
        button.set_icon_widget(image)

        self.main_window.show()
        gtk.main()


    def show_all_members(self):
        members = Person.select()
        self.show_members(members)


    def show_members(self, members):
        self.member_list.clear()
        for member in members:
            self.member_list.append(member.to_array() )


    def add_columns_to_tree_view(self, tree_view, person):
        """Add all of the List Columns to the member_tree_view"""
        column_number = 0
        for column_name in person.property_names:
            column = gtk.TreeViewColumn(column_name, gtk.CellRendererText(), text=column_number)
            column.set_resizable(True)

            if(column_name in person.hidden_properties):
                column.set_visible(False)

            tree_view.append_column(column)
            column_number += 1


    def on_search_button(self, widget):
        firstname = self.builder.get_object("firstname_search_entry").get_text()
        lastname = self.builder.get_object("lastname_search_entry").get_text()
        members = Person.get_by_name(firstname,lastname)
        self.show_members(members)


    def on_window_destroy(self, widget, data=None ):
        gtk.main_quit()


    def on_delete_member(self, widget):
        dialog = gtk.MessageDialog(self.main_window, gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_QUESTION,
                                   gtk.BUTTONS_OK_CANCEL,
                                   "Do you really want to delete this person?")
        result = dialog.run()
        dialog.destroy()

        if(result == gtk.RESPONSE_OK):
            selection = self.member_tree_view.get_selection()
            model, path = selection.get_selected()

            if path:
              person_id = model[path][0]
              self.member_list.remove(path)
              Person.delete(person_id)


    def on_clear_search(self, widget):
        self.builder.get_object("firstname_search_entry").set_text("")
        self.builder.get_object("lastname_search_entry").set_text("")
        self.show_all_members()


    def on_edit_member(self, widget, path = None, view_column = None):
        selection = self.member_tree_view.get_selection()
        model, path = selection.get_selected()

        if path:
            person_to_edit = Person.get(model[path][0])
            self.start_edit_dialoge(person_to_edit, path)


    def on_add_member(self, widget):
        self.start_edit_dialoge(None)


    def start_edit_dialoge(self, person_to_edit, place_in_tree_view = None):
        is_reading = False

        if self.card and not self.card.stopped:
            is_reading = True
            self.card.stop()

        add_edit_dialoge = member_window.Window(self.glade_file)
        result,new_member = add_edit_dialoge.run(person_to_edit)

        if (result == gtk.RESPONSE_OK and new_member):
            self.show_members([new_member])
        
        if(is_reading):
            self.card.start()


    def reading_card_result(self, input):
        if(self.blink):
            self.blink = False
            self.statusbar.push(1,"reading")
        else:
            self.blink = True
            self.statusbar.pop(1)
        print input


    def on_card_found(self, cardnumber):
        self.statusbar.pop(1)
        person = Person.get_by_cardnumber(cardnumber)
        person_list = list(person)
        if len(person_list):
            person_list[0].add_date()
            print "Member found :" + str(person_list[0].id)
            gobject.idle_add(self.start_edit_dialoge, person_list[0])
        else:
            print "No Member with cardnumber : " + cardnumber
            #TODO Start card reader again.


    def on_start_stop_rfid_reader(self,widget):
        if not self.card:
            print("No card reader")
            return

        button = self.builder.get_object("start_stop_button")
        if self.card.stopped:
            print "Start"
            button.set_label("Stop RFID reader")
            image = gtk.image_new_from_icon_name(gtk.STOCK_MEDIA_STOP, gtk.ICON_SIZE_BUTTON)
            image.show()
            button.set_icon_widget(image)
            self.card.start()
        else:
            self.statusbar.pop(1)
            print "Stop"
            button.set_label("Start RFID reader")
            image = gtk.image_new_from_icon_name("gtk-media-record", gtk.ICON_SIZE_BUTTON)
            image.show()
            button.set_icon_widget(image)
            self.card.stop()


    def quit(self, widget):
        self.card.stop()
        gtk.main_quit
        sys.exit(0)
