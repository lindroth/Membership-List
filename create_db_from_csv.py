#!/usr/bin/python
# This Python file uses the following encoding: utf-8
import sys
from lib.person import Person

filename = sys.argv[1]

#path = "/home/gny/Develop/eatingbits/membership_list/db/"
#sqlhub.processConnection = connectionForURI('sqlite:///'+ path +'new.db')


#Person.createTable(ifNotExists=True)

for line in open(filename,'r'):
    line = line.split(",")

    Person(firstname = line[0].strip(),
        lastname = line[1].strip(),
        cardnumber = "",
        payed = False,
        gender = 0,
        birthdate = line[2].strip(),
        streetname = "",
        post_address = "",
        email = line[3].strip(),
        sample = "")
