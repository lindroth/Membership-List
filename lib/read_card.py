import threading, thread
from threading import Thread, Lock
import gobject as gob
from time import sleep, time


class Card(Thread):

  def __init__(self, answer_to):
    print "created"
    self.main_app = answer_to
    self.ctrl = True
    self.Running = False
    self.lock = Lock()
    self.lock.acquire()
    Thread.__init__(self)

  def run(self):
    card_not_found = True
    while card_not_found:

      sleep(1)
      gob.idle_add(self.main_app, 10000)
      card_not_found = False

  def Start_Stop(self):
    print "start"
    if self.Running:
      self.Running = False
    else:
      try:
        self.lock.release()
      except thread_error:
        pass

  def Quit(self):
    self.ctrl = False
    if not self.Running:
      released = False
      while not released:
        try:
          self.lock.release()
          released = True
        except thread_error:
          pass
