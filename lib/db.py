from pysqlite2 import dbapi2 as sqlite
import os
from member import Member
from helpers import *

class Connection():
  
  def __init__(self,db_file = None):
    if db_file:
      self.connection = self._connect_with_file(db_file)
    else:
      self.connection = sqlite.connect(':memory:') 
 
    self.cursor = self.connection.cursor()


  def _connect_with_file(self,db_file):
    path = os.path.abspath(".")
    file_path = os.path.join(path + "/db",db_file)

    #Do we nead to create a new db?
    if os.path.isfile(file_path):
      return sqlite.connect(file_path)
    else:
      debug_print("No db file found. Setting up db")
      connection = sqlite.connect(file_path)
      self.setup()
      return connection


  def setup(self):
    self.cursor.execute('CREATE TABLE members ' + 
        '( id INTEGER PRIMARY KEY, firstname VARCHAR(50), ' + 
        'lastname VARCHAR(50), email VARCHAR(50))')
    self.connection.commit()


  def add_member(self, member):
    self.cursor.execute('INSERT INTO members VALUES (null,?,?,?)',
        (member.firstname, member.lastname, member.email) )
    self.connection.commit()
  
  def update_member(self, member):
    self.cursor.execute('UPDATE members SET firstname = ?, lastname = ?, email = ? ' +
        'WHERE id = ?',
        (member.firstname, member.lastname, member.email, member.id) )
    self.connection.commit()

  def find_member_by_id(self, id):
    self.cursor.execute('SELECT * FROM members WHERE id = ?', (id,))
    rows = self.cursor.fetchone()
    if rows:
      return self._row_to_members(rows)
    else:
      return None

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
      members.append( Member(row[1],row[2], row[3], row[0] ))
    return members

  def _row_to_members(self, row):
    return Member(row[1],row[2], row[3], row[0] )
