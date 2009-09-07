from pysqlite2 import dbapi2 as sqlite
from member import Member

class DB():
  def __init__(self,connection):
    self.connection = connection
  
  def setup(self,):
    self.cursor = self.connection.cursor()
    self.cursor.execute('CREATE TABLE members (id INTEGER PRIMARY KEY,name VARCHAR(50), email VARCHAR(50))')
    self.connection.commit()

  def add_member(self, member):
    self.cursor.execute('INSERT INTO members VALUES (null,?,?)',
        (member.name, member.email) )
    return self.connection.commit()

  def number_of_members(self):
    self.cursor.execute('SELECT * FROM members')
