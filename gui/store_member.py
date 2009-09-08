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

class Window:
  """This class is used to show wineDlg"""
	
  def __init__(self, wine="", winery="", grape=""):
	
    #setup the glade file
		self.gladefile = "member.glade"
		#setup the wine that we will return
		self.member = Member(wine,winery,grape)
		
  def run(self):
    """This function will show the wineDlg"""	
		
    builder = gtk.Builder()
    builder.add_from_file(self.gladefile)

		#Get the actual dialog widget
    self.store_member = builder.get_object("store_member")

		#Get all of the Entry Widgets and set their text
    firstname_entry = builder.get_object("firstname_entry")
    firstname_entry.set_text(self.member.firstname)

    lastname_entry = builder.get_object("lastname_entry")
    lastname_entry.set_text(self.member.lastname)

    email_entry = builder.get_object("email_entry")
    email_entry.set_text(self.member.email)

		#run the dialog and store the response		
    self.result = self.store_member.run()

		#get the value of the entry fields
    self.member.firstname = firstname_entry.get_text()
    self.member.lastname= lastname_entry.get_text()
    self.member.email= email_entry.get_text()
		
		#we are done with the dialog, destory it
    self.store_member.destroy()
		
		#return the result and the wine
    return self.result,self.member
