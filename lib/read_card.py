import threading, thread
import gobject, gtk

from time import sleep
from lib.rfid import RFID

class Card(object):


    def __init__(self, loop_callback, complete_callback=None):
        self.stopped = True
        self.loop_callback = loop_callback
        self.complete_callback = complete_callback
        self.rfid = RFID("/dev/ttyUSB0")


    def _start(self, *args, **kwargs):
        self.stopped = False
        cardnumber = None
        while not cardnumber:
            #read until card is found
            cardnumber = self.rfid.read_once()
            if self.stopped:
                thread.exit()
            sleep(0.1)
            gobject.idle_add(self._loop, "No Card found!")
        if self.complete_callback is not None:
            gobject.idle_add(self.complete_callback, cardnumber)
        thread.exit()

            
    def _write(self, cardnumber, dialog = None):
        self.stopped = False
        card_write_result = None
        while(card_write_result != "DONE!"):
            card_write_result = self.rfid.write(cardnumber)
            if self.stopped:
                thread.exit()
            sleep(0.1)

        dialog.destroy()
        thread.exit()


    def _loop(self, ret):
        if ret is None:
            ret = ()
        if not isinstance(ret, tuple):
            ret = (ret,)
        self.loop_callback(*ret)


    #TODO Change name to read
    def start(self, *args, **kwargs):
        threading.Thread(target=self._start, args=args, kwargs=kwargs).start()


    def write(self, cardnumber, dialog = None):
        threading.Thread(target=self._write, args=(cardnumber, dialog)).start()


    def stop(self):
        self.stopped = True
