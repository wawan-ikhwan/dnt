import socket
import struct

def int2ip(addr):
  '''
  Example:
  256 --> 0.0.1.0
  '''
  return socket.inet_ntoa(struct.pack("!I", addr))

def ip2int(addr):
  '''
  Example:
  0.0.1.0 --> 256
  '''
  return struct.unpack("!I", socket.inet_aton(addr))[0]