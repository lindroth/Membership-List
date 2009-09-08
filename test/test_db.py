#! /usr/bin/python
# This Python file uses the following encoding: utf-8
import sys
sys.path.append('../lib')
import unittest
import db
from member import Member

class TestMember(unittest.TestCase):
  
  def test_create_member(self):
    """Test the initialization of a member"""
    member = Member("Stig", u"Larsgård", "place@bo.com")
    self.assertTrue(member.firstname == "Stig")

class TestConnection(unittest.TestCase):
  
  def setUp(self):
    """Setting up the sqlite db, create table"""
    self.member_a = Member("Stig", u"Östgård", "stig@sing.com")
    self.member_b = Member("Arne", u"Låvenström", "arne@sing.com")
    self.db = db.Connection()
    self.db.setup()
    self.assertEqual(self.db.__class__,db.Connection)


  def test_add_member(self):
    """Add a member to the db"""
    self.db.add_member(self.member_a)


  def test_number_of_members(self):
    """Count numbers of members in db"""
    self.db.add_member(self.member_a)
    self.db.add_member(self.member_b)
    self.assertEqual(self.db.number_of_members(),2)


  def test_find_member_by_firstname(self):
    """Find a member by first name"""
    self.db.add_member(self.member_a)
    self.db.add_member(self.member_b)
    members = self.db.find_by_firstname(self.member_a.firstname)
    self.assertEqual(len(members), 1)
    self.assertTrue(members[0].firstname == self.member_a.firstname )


  def test_get_all_members(self):
    """Get all members from the db"""
    self.db.add_member(self.member_a)
    self.db.add_member(self.member_b)
    members = self.db.get_all_members()
    self.assertEqual(len(members), 2)
    for member in members:
      self.assertTrue(member.__class__ == Member)


  def tearDown(self):
    self.db.close()


if __name__ == '__main__':
  unittest.main()
