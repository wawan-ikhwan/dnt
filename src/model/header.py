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
  def _overwrite_bits(byte,bits,val,shift):
    if len(byte) > 1:
      raise('not a byte!')
    new_byte = bytearray(byte)
    new_byte[0] = new_byte[0] & ~((2**bits)-1 << shift)
    new_byte[0] = new_byte[0] | (val << shift)
    return new_byte
  
  @staticmethod
  def _get_bits(byte,bits,shift):
    if len(byte) > 1:
      raise('not a byte!')
    new_byte = bytearray(byte)
    new_byte[0] = new_byte[0] & ((2**bits)-1 << shift)
    new_byte[0] = new_byte[0] >> shift
    return new_byte
  
  @staticmethod
  def parse(header:bytes):
    header = bytearray(header[:1])
    return Header(
    en=bool(Header._get_bits(header,1,7)[0]),
    id=Header._get_bits(header,3,4)[0],
    tx=bool(Header._get_bits(header,1,3)[0]),
    seq=Header._get_bits(header,3,0)[0])
  
  def set_en(self,flag:bool=True):
    self.head = self._overwrite_bits(self.get_header(),1,int(flag),7)
  
  def set_id(self,id:int=0):
    self.head = self._overwrite_bits(self.get_header(),3,id,4)

  def set_tx(self,flag:bool=True):
    self.head = self._overwrite_bits(self.get_header(),1,int(flag),3)

  def set_seq(self,seq:int=0):
    self.head = self._overwrite_bits(self.get_header(),3,seq,0)
  
  def get_en(self):
    return self._get_bits(self.get_header(),1,7)[0]
  
  def get_id(self):
    return self._get_bits(self.get_header(),3,4)[0]
  
  def get_tx(self):
    return self._get_bits(self.get_header(),1,3)[0]
  
  def get_seq(self):
    return self._get_bits(self.get_header(),3,0)[0]

  def __init__(self,en:bool=True,id:int=0,tx:bool=False,seq:int=0):
    self.head = b'\x80'
    self.set_en(en)
    self.set_id(id)
    self.set_tx(tx)
    self.set_seq(seq)
  
  def get_header(self,object=False):
    if object: return Header.parse(self.get_header(object=False))
    return self.head