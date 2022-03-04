def overwrite_bits(byte,bits,val,shift):
  '''
  Overwriting allocated with new bit value in a bit position.
  Example:
  overwrite_bits(b'\x92',3,2,1) -> '\x94'
  '''
  if len(byte) > 1:
    raise('not a byte!')
  new_byte = bytearray(byte)
  new_byte[0] = new_byte[0] & ~((2**bits)-1 << shift)
  new_byte[0] = new_byte[0] | (val << shift)
  return new_byte

def get_bits(byte,bits,shift):
  '''
  Inverse of overwriting_bits, get_bits will return integer value according bit position.
  Example:
  10010100
  get_bits(b'\x94',3,1) -> 2
  '''
  if len(byte) > 1:
    raise('not a byte!')
  new_byte = bytearray(byte)
  new_byte[0] = new_byte[0] & ((2**bits)-1 << shift)
  new_byte[0] = new_byte[0] >> shift
  return new_byte