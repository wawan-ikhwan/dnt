from .int_bytes import int2bytes

def get_checksum(b: bytes):
  return int.to_bytes(b'\xff'[0]-int2bytes(sum(b))[0],1,'big')