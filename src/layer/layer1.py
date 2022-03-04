from ..utils.chunk import chunk
from ..utils.query import parse_query_answer4
from dnslib import DNSLabel, DNSRecord, DNSQuestion, QTYPE, CLASS
import socket

class DNTSocket:
  def __init__(self,domain:str='mip.my.id',dest:str='8.8.8.8',port:int=53):
    self.domain = domain
    self.dest = dest
    self.port = port
    self.PACKET_MAX_SIZE = 254 - len(DNSLabel(domain).idna()) - 4
    print('Packet Max Size:',self.PACKET_MAX_SIZE)

  def send(self,packet : bytes,getRecv=False): # biasanya max packet tidak boleh lebih dari 240 bytes
    if len(packet) > self.PACKET_MAX_SIZE: # Validasi packet
      print('Packet more than',self.PACKET_MAX_SIZE,'('+str(len(packet))+')')
      exit()
    fqdn = DNSLabel(self.domain)
    replacer = b'REPLACE THIS BRO'
    fqdn = fqdn.add(replacer)
    tanya = DNSRecord()
    tanya.add_question(DNSQuestion(qname=fqdn,qtype=QTYPE.A,qclass=CLASS.IN))
    bita = tanya.pack()
    buffer = b''
    for c in chunk(packet,63):
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
      sock.close()