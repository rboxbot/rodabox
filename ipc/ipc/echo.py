import sys
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as channel:
  channel.connect(('0.0.0.0', 7000))
  message = ' '.join(sys.argv[1:])
  channel.send(message.encode())
  print(channel.recv(100000))
