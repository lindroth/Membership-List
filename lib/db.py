from pysqlite2 import dbapi2 as sqlite
import os
from member import Member
from helpers import *

class Connection():
  
  def __init__(self,db_file = None):
    path = os.path.abspath(".")
    file_path = os.path.join(path + "/db",db_file)

    #Do we nead to create a new db?
    if os.path.isfile(file_path):
      db_file_exists = True
    else:
      db_file_exists = False

    if db_file:
      self.connection = sqlite.connect(file_path)
    else:
      self.connection = sqlite.connect(':memory:') 
 
    self.cursor = self.connection.cursor()

    #If we didn't have an db file we need to set it up.
    if not db_file_exists:
      debug_print("No db file found. Setting up db")
      self.setup()


  def setup(self):
    self.cursor.execute('CREATE TABLE members ' + 
        '( id INTEGER PRIMARY KEY, firstname VARCHAR(50), ' + 
        'lastname VARCHAR(50), email VARCHAR(50))')
    self.connection.commit()


  def add_member(self, member):
    self.cursor.execute('INSERT INTO members VALUES (null,?,?,?)',
        (member.firstname, member.lastname, member.email) )
    self.connection.commit()


  def number_of_members(self):
    self.cursor.execute('SELECT * FROM members')
    rows = self.cursor.fetchall()
    return len(rows)


  def find_by_firstname(self, firstname):
    self.cursor.execute('SELECT * FROM members WHERE firstname = ? ORDER BY firstname', (firstname,))
    rows = self.cursor.fetchall()
    return self._rows_to_members(rows)


  def get_all_members(self):
    self.cursor.execute('SELECT * FROM members ORDER BY firstname')
    rows = self.cursor.fetchall()
    return self._rows_to_members(rows)


  def close(self):
    self.connection.close()


  def _rows_to_members(self, rows):
    members = []
    for row in rows:
      members.append( Member(row[1],row[2], row[0]) )
    return members
