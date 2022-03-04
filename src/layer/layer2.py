from ..utils.query import parse_query_answer4
from .layer1 import DNTSocket
from ..model.packet import Packet
from ..model.segment import Segment

class DNTConnect(DNTSocket):
  def __init__(self,segment:Segment,domain:str='mip.my.id',dest:str='8.8.8.8',port:int=53):
    super().__init__(domain,dest,port)
    self.MAX_SEQ = 7 # ketetapan protokol
    self.MAX_SEGMENT_LEN = ((self.PACKET_MAX_SIZE-1) * (self.MAX_SEQ+1))
    self.segment = segment
    self.id = None
  
  def send_handshake(self):
    self.id = parse_query_answer4(self.send(packet=Packet(en=True,id=0,tx=False,seq=1,max_packet_size=self.PACKET_MAX_SIZE,data=self.segment.get_metadata()).get_packet(),getRecv=True))
    return self.id
  
  def send_segment(self):
    if self.id is not None:
      for p in self.segment.get_packets():
        p.set_id(self.id)
        p.set_tx(True)
        self.send(p.get_packet(),getRecv=False)
  
  def send_close(self):
    if self.id is not None:
      return parse_query_answer4(self.send(Packet(en=True,id=self.id,tx=False,seq=2,max_packet_size=self.PACKET_MAX_SIZE),getRecv=True))