# This Python file uses the following encoding: utf-8
import sys
from lib.person import Person

filename = sys.argv[1]

#path = "/home/gny/Develop/eatingbits/membership_list/db/"
#sqlhub.processConnection = connectionForURI('sqlite:///'+ path +'new.db')


Person.createTable(ifNotExists=True)

for line in open(filename,'r'):
    line = line.split(",")

    if "0" in line[2]:
        gender = False
    else:
        gender = True

    if "1" in line[0]:
        payed = True
    else:
        payed = False

    Person(firstname = line[1],
        lastname = line[3],
        cardnumber = "",
        payed = payed,
        gender = gender,
        birthdate = line[4],
        streetname = line[5],
        post_address = line[6],
        email = line[7],
        sample = "")
