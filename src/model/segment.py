from ..utils.chunk import chunk
from ..utils.checksum import get_checksum
from .metadata import Metadata
from .packet import Packet
class Segment(Metadata):
  '''
  A segment.
  '''

  def __init__(self,data=b'',ttl:int=7,max_seq:int=7,f:bool=False,max_packet_size:int=240):
    # max_seq in segment argument is just threeshold
    # real max_seq is calculated automatically by superclass (Metadata)
    if len(data) > (max_packet_size-1)*(max_seq+1):
      print('WARNING! DATA (',len(data),') MORE THAN',(max_packet_size-1)*max_seq)
      raise('Segment exceed limit!')
    self.packets = [Packet(en=True,tx=True,seq=sq,data=dat,max_packet_size=max_packet_size) for sq,dat in enumerate(chunk(data,max_packet_size-1)) if sq <= max_seq]
    super().__init__(len(data),ttl,len(self.packets)-1,get_checksum(data),f)
  
  def get_packets(self):
    return self.packets