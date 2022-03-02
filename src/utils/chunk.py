def chunk(data,w):
  '''
  Split data into few chunk.
  eg: chunk('hello',2) --> [he,ll,o]
  '''
  return [data[i:i+w] for i in range(0, len(data), w)]