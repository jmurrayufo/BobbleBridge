# Normal Modules
import sys
import os
import socket

# Custom Modules
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\obj'
sys.path.append(basedir)
from Connection import *

def Main( ):
    # Run test code!
   HOST = ''               # Symbolic name meaning all available interfaces
   PORT = 56464              # Arbitrary non-privileged port
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.bind( (HOST, PORT) )

   print "Begin Listen"
   s.listen( 5 )
   s.settimeout( 0 )
   pool = list()
   while True:

      try:
         conn, addr = s.accept()
      except( socket.timeout, socket.error ):
         pass
      else:
         print 'Connected by', addr
         pool.append( Connection( conn, addr ) )
     
      for idx,val in enumerate( pool ):
         # print "Check",val
         try:
            val.Recv( )
         except( socket.error ):
            pass
         if( val.Data ):
            print "Check",val
            print " Got:",val.Data
         else:
            if( val.Stale( 5 ) ):
               print "Check",val
               print " TO!"
               print " Removed!",val
               print " Age:",val.Age()
               print val.Stale( 5 )
               del pool[idx]
         try:
            val.Send( val.Data )
         except( socket.error ):
            print " Cannot send! Delete!"
            del pool[idx]
   raw_input()


if __name__=='__main__':
   Main()