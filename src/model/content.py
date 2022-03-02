from .segment import Segment
class Content:
  '''
  Content that will send through buffers
  '''

  @staticmethod
  def _chunk(data,w):
    '''
    Split data into few chunk.
    eg: chunk('hello',2) --> [he,ll,o]
    '''
    return [data[i:i+w] for i in range(0, len(data), w)]

  def __init__(self,content:bytes=b'', payload_max_size:int=240):
    '''
    content: data that will send
    payload_max_size: maximum payload size
    '''
    self._segment_max_size = payload_max_size-1 # -1 karena header tidak dihitung

    self._chunked_segment = self._chunk(content,self._segment_max_size)
    self.segments = [Segment(s) for s in self._chunk(self._chunked_segment,8)]
    self.content_length=len(content)
  
  def get_segments(self):
    return self.segments