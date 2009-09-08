class Member(object):
  def __init__(self, firstname, lastname, email, id = None):
    self.id = id
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
    #personnr, postnr, postort ,address, medlemsnr, email, rfid. 
  def parameters_to_array(self):
    return [self.firstname, self.lastname, self.email]
