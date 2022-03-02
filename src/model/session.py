from .metadata import Metadata


class Session:

  def __init__(self):
    self.id = {0:b'',1:b'',2:b'',3:b'',4:b'',5:b'',6:b'',7:b''}

  def get_available_id(self):
    return self.find_empty_id()

  def find_empty_id(self):
    for id,buffer in self.id.items():
      if len(buffer) == 0:
        return id
  
  def on_handshake(metadata:Metadata):
    pass

  # def get_handshake(self,):


s = Session()
print(s.find_empty_id())