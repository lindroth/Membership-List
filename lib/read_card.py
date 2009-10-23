import threading, thread
import gobject, gtk

from time import sleep

class Card(object):

   def __init__(self, loop_callback, complete_callback=None):
       self.loop_callback = loop_callback
       self.complete_callback = complete_callback

   def _start(self, *args, **kwargs):
       self._stopped = False
       card_not_found = True
       while card_not_found:
          #read until card is found
           if self._stopped:
               thread.exit()
           sleep(1) 
           gobject.idle_add(self._loop, "Not found!")
       if self.complete_callback is not None:
           gobject.idle_add(self.complete_callback, 10000)

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

