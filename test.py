import unittest
from pysqlite2 import dbapi2 as sqlite
import DB
from member import Member

class TestDB(unittest.TestCase):
  
  def setUp(self):
    """Setting up the sqlite db, create table"""
    connection = sqlite.connect(':memory:') 
    self.db = DB.DB(connection)
    self.db.setup()
    self.assertEqual(self.db.__class__,DB.DB)
 
  def test_add_member(self):
    """Add a member to the db"""
    member_a = Member("Stig", "stig@sing.com")
    self.assertTrue( self.db.add_member(member_a) )

  def test_number_of_members(self):
    member_a = Member("Stig", "stig@sing.com")
    self.assertTrue( self.db.add_member(member_a) )
    self.assertEqual(1,self.db.number_of_members())



if __name__ == '__main__':
  unittest.main()
    


