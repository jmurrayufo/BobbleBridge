# Echo client program
import socket
import time

HOST = 'localhost'    # The remote host
PORT = 56464              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect((HOST, PORT))
for i in range(10):  
   s.sendall('Hello, world'+str(i) )
   data = s.recv(1024)
   print 'Received', repr(data)
   time.sleep(0.1)
# s.close()