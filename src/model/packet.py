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

  def __init__(self,en:bool=True,id:int=0, tx:bool=False, seq:int=0,data:bytes=b'',max_packet_size:int=240):
    '''Initializing instance of Client Packet with setting header'''
    super().__init__(en=en,id=id,tx=tx,seq=seq)
    self.data = data
    self.packet = self.get_header()+self.data
    if len(self.packet) > max_packet_size:
      raise('Packet size exceed limit!')
  
  def set_data(self,data:bytes):
    '''
    Actual bytes data to send.
    data: metadata if op, real binary data if tx.
    '''
    self.data = data
    self.packet = self.get_header()+self.data
  
  def get_data(self):
    '''Get bytes of data.'''
    return self.data

  def get_packet(self) -> bytes:
    '''Get bytes of packet.'''
    self.packet = self.get_header()+self.data
    return self.packet