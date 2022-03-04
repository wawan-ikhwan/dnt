from dotenv import dotenv_values
from src.model.segment import Segment
ENV = dotenv_values('.env')
print(ENV)
from src.layer.layer1 import DNTSocket
from src.layer.layer2 import DNTConnect

f = open('./bin/preambule_uud.txt','rb').read()

conn = DNTConnect(Segment(f[:50]),ENV['DOMAIN'],ENV['RESOLVER'])
print(conn.send_handshake())
conn.send_segment()

exit()

sock = DNTSocket(ENV['DOMAIN'],ENV['RESOLVER'])
sock.send(b'hello')
