from .int_ipv4 import ip2int
from .chunk import chunk
from dnslib import DNSRecord

def parse_query_domain(d:bytes,leftDom:str='mip'):
  '''
  Filter DNS domain byte to real byte data
  example:
  blablabla\xaf\xfa\xfa.mip.my.id.blabla --> \xaf\xfa\xfa
  '''
  try:
    d = d[12:d.rfind(leftDom.encode())-1]
    d = chunk(d,64)
    d = [ i[1:] for i in d ]
    d = b''.join(d)
    return d
  except: return b''

def parse_query_answer4(d:bytes) -> int:
  '''
  Filter rdata of A (ipv4) to int
  example:
  blablabla\xaf\xfa\xfa.mip.my.id.blabla0.0.1.0 --> 256
  '''
  try:
    return ip2int(str(DNSRecord.parse(d).get_a().rdata))
  except: return None