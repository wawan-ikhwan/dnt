from ..utils.chunk import chunk
from .segment import Segment
class Content: # Need update
  '''
  Content that will send through buffers
  '''

  def __init__(self,content:bytes=b'', payload_max_size:int=240):
    '''
    content: data that will send
    payload_max_size: maximum payload size
    '''
    self._segment_max_size = payload_max_size-1 # -1 karena header tidak dihitung
    self._chunked_segment = chunk(content,self._segment_max_size)

    self.segments = [Segment(s) for s in chunk(self._chunked_segment,8)]
    self.content_length=len(content)
    self.content = content
  
  def get_segments(self):
    return self.segments
  
  def get_content(self):
    return self.content