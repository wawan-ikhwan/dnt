from ..utils.bits import overwrite_bits,get_bits

class Header:

  '''
  |0 |  1 2 3  |    4   |   5 6 7   |
  |en|    id   |  op/tx |opcode/seq |
  Header of Client Packet.
  en: Mandatory bit that must be set to True.
  id: Client ID
  tx: transmit mode if True , operation mode if False.
  seq: sequence if tx, opcode if op.
  '''
  
  @staticmethod
  def parse(header:bytes):
    header = bytearray(header[:1])
    return Header(
    en=bool(get_bits(header,1,7)[0]),
    id=get_bits(header,3,4)[0],
    tx=bool(get_bits(header,1,3)[0]),
    seq=get_bits(header,3,0)[0])
  
  def set_en(self,flag:bool=True):
    self.head = overwrite_bits(self.get_header(),1,int(flag),7)
  
  def set_id(self,id:int=0):
    self.head = overwrite_bits(self.get_header(),3,id,4)

  def set_tx(self,flag:bool=True):
    self.head = overwrite_bits(self.get_header(),1,int(flag),3)

  def set_seq(self,seq:int=0):
    self.head = overwrite_bits(self.get_header(),3,seq,0)
  
  def get_en(self):
    return get_bits(self.get_header(),1,7)[0]
  
  def get_id(self):
    return get_bits(self.get_header(),3,4)[0]
  
  def get_tx(self):
    return get_bits(self.get_header(),1,3)[0]
  
  def get_seq(self):
    return get_bits(self.get_header(),3,0)[0]

  def __init__(self,en:bool=True,id:int=0,tx:bool=False,seq:int=0):
    self.head = b'\x80'
    self.set_en(en)
    self.set_id(id)
    self.set_tx(tx)
    self.set_seq(seq)
  
  def get_header(self,inObject=False):
    if inObject: return Header.parse(self.get_header(inObject=False))
    return self.head