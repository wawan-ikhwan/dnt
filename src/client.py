from dnslib import DNSRecord, DNSQuestion, DNSLabel, QTYPE, CLASS

from time import sleep

import socket
import struct

from .model.segment import Segment
from .model.packet import Packet

def ip2int(addr):
  return struct.unpack("!I", socket.inet_aton(addr))[0]
def int2ip(addr):
  return socket.inet_ntoa(struct.pack("!I", addr))

def without_keys(d, keys):
  return {x: d[x] for x in d if x not in keys}

class Client:

  @staticmethod
  def _chunk(data,w):
    '''
    Split data into few chunk.
    eg: chunk('hello',2) --> [he,ll,o]
    '''
    return [data[i:i+w] for i in range(0, len(data), w)]

  def __init__(self,domain:str='mip.my.id',dest:str='8.8.8.8',port:int=53):
    self.domain = domain
    self.dest = dest
    self.port = port
    self.PACKET_MAX_SIZE = 254 - len(DNSLabel(domain).idna()) - 4
    print('Packet Max Size:',self.PACKET_MAX_SIZE)

  def send_raw_packet(self,packet : bytes,getRecv=False): # biasanya max packet tidak boleh lebih dari 240 bytes
    if len(packet) > self.PACKET_MAX_SIZE: # Validasi packet
      print('Packet more than',self.PACKET_MAX_SIZE,'('+str(len(packet))+')')
      return
    fqdn = DNSLabel(self.domain)
    replacer = b'REPLACE THIS BRO'
    fqdn = fqdn.add(replacer)
    tanya = DNSRecord()
    tanya.add_question(DNSQuestion(qname=fqdn,qtype=QTYPE.A,qclass=CLASS.IN))
    bita = tanya.pack()
    buffer = b''
    for c in self._chunk(packet,63):
      buffer += int.to_bytes(len(c),1,'big') + c
    bita = bita.replace(b'\x10'+replacer,buffer)
    try:
      sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      # print(bita)
      sock.sendto(bita,(self.dest,self.port))
      if getRecv:
        recv,_ = sock.recvfrom(512)
        return recv
    except Exception as e: print(e)
    finally: 
      sleep(1)
      sock.close()
  
  def send_packet(self, packet: Packet,get_resp:bool=False):
    return self.send_raw_packet(packet.pack(), getRecv=get_resp)

  def send_segment(self,segment:Segment):
    packets = segment.get_packets()
    id = self.handshake(segment)
    print('ID:',id)
    for p in packets:
      p.set_id(id)
      print(p.pack()[:5])
      self.send_packet(p,get_resp=False)
    print(self.close(id))

  def handshake(self,segment:Segment):
    '''
    Get available ID (establishing)
    '''
    try:
      print(segment.get_metadata(object=True))
      answer = self.send_packet(Packet(tx=False,seq=1,data=segment.get_metadata()),get_resp=True)
      answer = DNSRecord.parse(answer).get_a()
      return ip2int(str(answer.rdata))
    except Exception as e:
      print('Handshake failed,',e,', retrying...')
      sleep(3)
      return self.handshake(segment)
  
  def close(self,id:int):
    try:
      p = Packet(tx=False,seq=2,id=id,data=b'\xff')
      print('Closing:',p.pack())
      answer = self.send_packet(p,get_resp=True)
      answer = DNSRecord.parse(answer).get_a()
      if answer.rdata is None: return 1
      elif ip2int(str(answer.rdata)) == 0: return 0
      else: return 1
    except:
      print('Close failed, retrying...')
      sleep(3)
      return self.close(id)

# f = open('DNT_PROTOCOL.xlsx','rb').read()
# c.send_packet(id=2,tx=True,seq=1,data=b'\xff\xfa')

# print(c.send_raw_packet(b'',getRecv=True))
