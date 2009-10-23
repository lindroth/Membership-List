#! /usr/bin/python
# This Python file uses the following encoding: utf-8
import sys
sys.path.append('../lib')
import unittest
from person import Person
from member import Member

class TestPerson(unittest.TestCase):
  
  def setUp(self):
    connection = 'sqlite:/:memory:'
    Person.createTable()
    a = Person(firstname = 'test',lastname ='sda')
    print Person.get(1)
  
  def test_af(self):
    pass
if __name__ == '__main__':
  unittest.main()
