from dnslib import DNSRecord, DNSLabel,RR, AAAA, A, QTYPE
from dnslib.server import DNSServer, DNSLogger, DNSHandler
from time import sleep
from random import randint

import socket
import struct

from src.model.packet import Packet
from src.model.metadata import Metadata

def ip2int(addr):
  return struct.unpack("!I", socket.inet_aton(addr))[0]
def int2ip(addr):
  return socket.inet_ntoa(struct.pack("!I", addr))

def chunk(data,w):
  '''
  Split data into few chunk.
  eg: chunk('hello',2) --> [he,ll,o]
  '''
  return [data[i:i+w] for i in range(0, len(data), w)]

def parse_query(d:bytes,tld:str='mip'):
  '''
  Filter DNS Header byte to real byte data
  '''
  try:
    d = d[12:d.rfind(tld.encode())-1]
    d = chunk(d,64)
    d = [ i[1:] for i in d ]
    d = b''.join(d)
    return d
  except: return b''

class Penangan(DNSHandler):
  """
    Handler for socketserver. Transparently handles both TCP/UDP requests
    (TCP requests have length prepended) and hands off lookup to resolver
    instance specified in <SocketServer>.resolver
  """

  udplen = 0                  # Max udp packet length (0 = ignore)

  def get_reply(self,data):
    request = DNSRecord.parse(data)
    self.server.logger.log_request(self,request)

    resolver = self.server.resolver
    reply = resolver.resolve(request,self)
    self.server.logger.log_reply(self,reply)

    if reply is None: return
    if self.protocol == 'udp':
      rdata = reply.pack()
      if self.udplen and len(rdata) > self.udplen:
        truncated_reply = reply.truncate()
        rdata = truncated_reply.pack()
        self.server.logger.log_truncated(self,truncated_reply)
    else:
      rdata = reply.pack()

    return rdata

class Penyelesai:
  def __init__(self,tunDom:str='mip.my.id',ip:str='27.112.79.120',mainLabel='mip'):
    if not (mainLabel in tunDom): raise('No mainLabel in domain')
    self.tun = DNSLabel(tunDom)
    self.mainLabel = 'mip'
    tun=self.tun.idna()
    zone = RR.fromZone(self.tun.idna()+' 600 IN SOA '+tun+' root.'+tun+' 42 600 600 600 600')
    zone.append(*RR.fromZone(tun+' 60 IN NS ns1.'+tun))
    zone.append(*RR.fromZone(tun+' 60 IN NS ns2.'+tun))
    zone.append(*RR.fromZone(tun+' 60 IN A '+ip))
    zone.append(*RR.fromZone('ns1.'+tun+' 60 IN A '+ip))
    zone.append(*RR.fromZone('ns2.'+tun+' 60 IN A '+ip))
    zone.append(*RR.fromZone('ns1.'+tun+' 60 IN AAAA 2001:67c:2b0:db32:0:1:1b70:4f78'))
    zone.append(*RR.fromZone('ns2.'+tun+' 60 IN AAAA 2001:67c:2b0:db32:0:1:1b70:4f78'))
    self.zone=zone

  def resolve(self, req : DNSRecord, _):
    jawab =  req.reply()

    qn = jawab.get_q().get_qname()
    qt = jawab.get_q().qtype
    qc = jawab.get_q().qclass

    print(qn)

    subdomain = parse_query(req.pack(),tld=self.mainLabel)

    if len(subdomain) == 0:
      jawab.add_answer(RR(qn,qt,qc,ttl=0,rdata=A('1.0.0.0')))
      return jawab

    packet = Packet.parse(subdomain)

    if packet.get_en() == False: return jawab

    print(packet.get_header(),packet.get_data()[:5])

    # =======================SESSIONING==================
    if qt == QTYPE.A:
      if packet.get_tx() == 0 and packet.get_seq() == 1: # ON HANDSHAKE
        id = randint(0,7)
        print('Metadata received,',Metadata.parse(packet.get_data()).__dict__)
        print('Handshaked, ID =',id)
        jawab.add_answer(RR(qn,qt,qc,ttl=0,rdata=A(int2ip(id))))
        return jawab
      elif packet.get_tx() == 1: # ON TRANSMIT
        return jawab
      elif packet.get_tx() == 0 and packet.get_seq() == 2: # ON CLOSE
        print('Closed!',packet.get_id())
        return jawab

    return jawab

    #   for rr in self.zone:
    #     if qn == rr.rname and qt == rr.rtype:
    #       jawab.add_answer(rr)

try:
  server = DNSServer(Penyelesai(),'10.5.143.3',53,tcp=False,logger=DNSLogger(log='-data,-recv,-send,-request,-reply, -invalid request',prefix=False),handler=Penangan)
  print('Public')
except:
  server = DNSServer(Penyelesai(),'127.0.0.1',53,tcp=False,logger=DNSLogger(log='-data,-recv,-send,-request,-reply, -invalid request',prefix=False),handler=Penangan)
  print('Local')
server.start_thread()

try: 
  while True: sleep(5)
except: pass
server.stop()
