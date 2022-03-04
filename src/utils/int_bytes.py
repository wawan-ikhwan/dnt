def int2bytes(x: int) -> bytes:
  return x.to_bytes((x.bit_length() + 7) // 8, 'big')