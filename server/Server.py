# Echo server program
import socket

HOST = ''               # Symbolic name meaning all available interfaces
PORT = 56464              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print "Begin Listen"
s.listen( 1 )
print "End Listen"
s.settimeout(1)
while True:
   print "Try..."
   s.settimeout(1)
   print s.gettimeout()
   try:
      conn, addr = s.accept()
   except( socket.timeout ):
      continue
   print 'Connected by', addr
   s.settimeout( None )
   while 1:
      try:
         data = conn.recv(1024)
      except( socket.error ):
         continue
      if not data: break
      conn.sendall(data)
   conn.close()
raw_input()