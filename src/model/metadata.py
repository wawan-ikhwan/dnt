from ..utils.bits import get_bits

class Metadata:
  '''
  ttl: actually reserved nibble
  f: actually reserved flag
  '''

  @staticmethod
  def parse(metadata:bytes):
    return Metadata(
      segment_length = int.from_bytes(metadata[:2],'big'),
      ttl = int.from_bytes(get_bits(metadata[2:3],4,4),'big'),
      max_seq = int.from_bytes(get_bits(metadata[2:3],3,0),'big'),
      f =  bool(int.from_bytes(get_bits(metadata[2:3],1,3),'big')),
      chksum=metadata[3:]
    )

  def __init__(self,segment_length:int,ttl:int,max_seq:int,chksum:bytes,f:bool=False):
    self.segment_length =  segment_length
    self.ttl = ttl
    self.max_seq = max_seq
    self.chksum = chksum
    self.f = f

  def get_metadata(self,object=False):
    # print(self.segment_length,self.ttl,self.f,self.max_seq,self.chksum)
    if object: return Metadata.parse(self.get_metadata(object=False))
    meta1 = int.to_bytes(self.segment_length,2,'big')
    meta3 = int.to_bytes((self.ttl << 4)+((int(self.f) << 3 )+self.max_seq),1,'big')
    meta4 = self.chksum
    return meta1+meta3+meta4
  
  def __repr__(self):
      return str(self.__dict__)

# print(Metadata.parse(b'\x05\xa6\x16\xfd').get_metadata())