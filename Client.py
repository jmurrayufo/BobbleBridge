# Echo client program
import socket
import time

HOST = '192.168.1.106'    # The remote host
PORT = 56464              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
s.connect((HOST, PORT))
strOut = ''
for i in range(4096):
   strOut += 'a'
# print strOut
for i in range(10000):  
   s.sendall(strOut)
   data = s.recv(4096)
   # print 'Received', repr(data)
   # time.sleep(0.1)
# s.close()