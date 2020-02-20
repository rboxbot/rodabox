import sys
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
  channel.connect(('0.0.0.0', 8001))
  message = ' '.join(sys.argv[1:])
  channel.send(message.encode())
  rec = channel.recv(100000)
  print(rec)
