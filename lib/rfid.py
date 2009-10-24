#!/usr/bin/python
import serial
import time
import os

class RFID:


  def __init__(self, serial_device):
    self.serial = serial.Serial(serial_device, 9600, timeout = 2)


  def read(self):
    while(True):
      x = "ER1!"
      while(x == "ER1!" or x == "ER3!" or x == "ER5!"):
        self.serial.write("Da0106!")
        x = self.serial.readline(eol="!")
        kortnummer = x[25:32]
      return kortnummer


  def write(self,inputstring):
    pass


  def stop(self):
    self.serial.close()
