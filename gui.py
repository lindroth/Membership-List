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

class Member:

  def __init__(self):
    builder = gtk.Builder()
    builder.add_from_file("member.glade")
    dic = { 
        "on_buttonQuit_clicked" : self.quit,
        "on_window_destroy" : self.quit,
    }
    builder.connect_signals(dic)
    self.window = builder.get_object("window")
    self.window.show()

  
  def on_window_destroy(self, widget, data=None ):
    gtk.main_quit()


  def add(self):
    pass


  def quit(self, widget):
    gtk.main_quit
    sys.exit(0)

if __name__ == "__main__":
  app = Member()
  gtk.main()
    
