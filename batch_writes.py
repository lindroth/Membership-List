#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import sys
from lib.rfid import RFID

#number = int(sys.argv[1])
import time
number = 12
rfid = RFID("/dev/ttyUSB1")
current_number = 0

while True:

    time.sleep(0.1)

    try:
        current_number = int(rfid.read_once())
    except:
        pass

    if(current_number + 1 != number):
        result = rfid.write(str(number))
        if(result == "DONE!"):
            print "Successfully writen " + str(number) + " to card"
            number += 1






