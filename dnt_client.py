from dotenv import dotenv_values
ENV = dotenv_values('.env')
print(ENV)
from src.layer1.dnt_socket import DNTSocket

sock = DNTSocket(ENV['DOMAIN'],ENV['RESOLVER'])
sock.send(b'hello')
