from .header import Header

class Packet(Header):

  @staticmethod
  def parse(packet:bytes):
    header = Header.parse(packet[:1])
    return Packet(
    en=bool(header.get_en()),
    id=header.get_id(),
    tx=bool(header.get_tx()),
    seq=header.get_seq(),
    data=packet[1:])

  def __init__(self,en:bool=True,id:int=0, tx:bool=False, seq:int=0,data:bytes=b''):
    '''Initializing instance of Client Packet with setting header'''
    super().__init__(en=en,id=id,tx=tx,seq=seq)
    self.data = data
    self.packet = self.get_header()+self.data
  
  def set_data(self,data:bytes):
    '''
    Actual bytes data to send.
    data: metadata if op, real binay data if tx.
    '''
    self.data = data
    self.packet = self.get_header()+self.data
  
  def get_data(self):
    return self.data

  def pack(self):
    '''Get bytes of packet.'''
    self.packet = self.get_header()+self.data
    return self.packet

# p = Packet(en=True,tx=True,id=0,seq=0)
# p.set_id(1)
# p.set_tx(False)
# print(p.pack())