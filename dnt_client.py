from dotenv import dotenv_values
from src.model.segment import Segment
ENV = dotenv_values('.env')
from src.layer.layer1 import DNTSocket
from src.layer.layer2 import DNTConnect
from time import sleep

# f = open('./bin/preambule_uud.txt','rb').read()
f = b"A"*239*8
# max byte that able to send is 239*8
conn = DNTConnect(Segment(f),ENV['DOMAIN'],ENV['RESOLVER'])
print(conn.send_handshake())
conn.send_segment()
print(conn.send_close())

exit()

# sock = DNTSocket(ENV['DOMAIN'],ENV['RESOLVER'])
# sock.send(b'hello')
