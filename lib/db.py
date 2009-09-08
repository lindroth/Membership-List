from pysqlite2 import dbapi2 as sqlite
from member import Member

class Connection():
  
  def __init__(self,db_file = None):
    if db_file:
      pass
    else:
      self.connection = sqlite.connect(':memory:') 
  

  def setup(self,):
    self.cursor = self.connection.cursor()
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
