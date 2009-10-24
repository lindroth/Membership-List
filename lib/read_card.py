import threading, thread
import gobject, gtk

from time import sleep
from lib.rfid import RFID

class Card(object):


   def __init__(self, loop_callback, complete_callback=None):
       self.loop_callback = loop_callback
       self.complete_callback = complete_callback
       self.rfid = RFID("/dev/ttyUSB0")


   def _start(self, *args, **kwargs):
       self._stopped = False
       cardnumber = None
       while not cardnumber:
          #read until card is found
          cardnumber = self.rfid.read_once()
          if self._stopped:
               thread.exit()
          sleep(0.5) 
          gobject.idle_add(self._loop, "No Card found!")
       if self.complete_callback is not None:
           gobject.idle_add(self.complete_callback, cardnumber)


   def _loop(self, ret):
       if ret is None:
           ret = ()
       if not isinstance(ret, tuple):
           ret = (ret,)
       self.loop_callback(*ret)


   def start(self, *args, **kwargs):
       threading.Thread(target=self._start, args=args, kwargs=kwargs).start()


   def stop(self):
       self._stopped = True

