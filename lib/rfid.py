#!/usr/bin/python
import serial
import time
import os

class RFID:

    error_codes = ["ER1!","ER2!","ER3!","ER4!","ER5!"]


    def __init__(self, serial_device):
        self.serial = serial.Serial(serial_device, 9600, timeout = 2)
        #self.serial = serial.Serial(timeout = 2)


    def read_once(self):
        self.serial.write("Da0106!")
        card_number = self.serial.readline(eol="!")
        if card_number in RFID.error_codes:
            return None
        else:
            card_number = card_number.rstrip("\!")
            card_number = card_number.lstrip("CBAB666")
            card_number = card_number.lstrip("0")            
            return card_number


    def read(self):
        while(True):
            x = "ER1!"
            while(x in RFID.error_codes):
                self.serial.write("Da0106!")
                x = self.serial.readline(eol="!")
                kortnummer = x[25:32]
            return kortnummer

    def write(self,inputstring):
        x = "ER1!"
        inputstring = inputstring.zfill(25)
        inputstring = "CBAB666" + inputstring
        self.serial.write("Db0106" + inputstring + "!")
        x = self.serial.readline(eol="!")
        return x

    def stop(self):
        self.serial.close()