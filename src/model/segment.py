from .metadata import Metadata
from .packet import Packet
class Segment(Metadata):
  '''
  A segment.
  '''

  @staticmethod
  def _int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

  @staticmethod
  def _get_checksum(b: bytes):
    return int.to_bytes(b'\xff'[0]-Segment._int_to_bytes(sum(b))[0],1,'big')

  def __init__(self,segment:list[bytes],ttl=7,f=False):
    self.segment = segment
    max_seq = len(self.segment)-1
    bita = b''.join(self.segment)
    segment_length = len(bita)-1
    chksum = Segment._get_checksum(bita)
    self.packets = [Packet(en=True,tx=True,seq=i,data=self.segment[i]) for i in range(max_seq)]

    super().__init__(segment_length,ttl,max_seq,chksum,f)
  
  def get_packets(self):
    return self.packets