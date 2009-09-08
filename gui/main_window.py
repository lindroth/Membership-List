# This Python file uses the following encoding: utf-8
import sys

try:  
        import pygtk  
        #pygtk.require("2.0")  
except:  
        pass  
try:  
        import gtk  
except:  
        print("GTK Not Availible")
        sys.exit(1)

from store_member import Add

class Window:

  def __init__(self):
    member_properties = [
        "Firstname", "Lastname","email"]
  
    builder = gtk.Builder()
    builder.add_from_file("member.glade")

    signals = { 
        "on_buttonQuit_clicked" : self.quit,
        "on_window_destroy" : self.quit,
        "on_add_member" : self.on_add_member,
    }
    builder.connect_signals(signals)

    self.member_tree_view = builder.get_object("memberview")
    self.add_columns_to_tree_view(self.member_tree_view,member_properties)
	
    self.member_list = gtk.ListStore(str, str, str)
    self.member_tree_view.set_model(self.member_list)	
    
    self.main_window = builder.get_object("main_window")
    self.main_window.show()
   
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
		list_store.append_column(column)


  def on_window_destroy(self, widget, data=None ):
    gtk.main_quit()

	
  def on_add_member(self, widget):
    """Called when the use wants to add a wine"""
    #Cteate the dialog, show it, and store the results
		
    add_member_dialog = Store()
    result,new_member = add_member_dialog.run()

    if (result == gtk.RESPONSE_OK):
		#	"""The user clicked Ok, so let's add this
		#	wine to the wine list"""
		#	self.wineList.append(newWine.getList())
      self.member_list.append(new_member.parameters_to_array())


  def quit(self, widget):
    gtk.main_quit
    sys.exit(0)

if __name__ == "__main__":
  app = Member()
  gtk.main()
    
