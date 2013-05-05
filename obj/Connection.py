import time
import socket

class Connection():
   """
   Server needs to maintain a variable amount of connections to the client space. These
   objects will keep track of those connections, and handle timeouts
   """
   def __init__( self, conn, addr ):
      self.Conn = conn
      self.Addr = addr
      self.FirstHeard = time.time()
      self.LastHeard = time.time()
      self.Data = 0
      self.In = 0
      self.Out = 0

   def __del__( self ):
      # Lets be nice and try to close the connection when we are deleted
      self.Conn.close()

   def __str__( self ):
      return "%s:%d"%( self.Addr[0], self.Addr[1] )

   def __repr__( self ):
      return self.__str__( )

   def Recv( self, size = 4096 ):
      self.Data = str()
      try:
         self.Data = self.Conn.recv( size )
      except( socket.error ):
         return


      if( self.Data ):
         self.LastHeard = time.time()
         self.In += len( self.Data )

   def Send( self, data ):
      self.Conn.sendall( data )
      self.Out += len( data )

   def Age( self ):
      return time.time() - self.FirstHeard

   def Stale( self, sellBy = 10 ):
      """
      Is this connection stale? We compare sellBy to the last time we heard from it 
      (default wait time is 10 seconds) and return True if it is stale, false if not.
      """
      if( time.time() - self.LastHeard > sellBy ):
         return True
      return False

   def Close( self ):
      self.Conn.close()



# Place holder test code
if __name__ == '__main__':
   # Run test code!
   HOST = ''               # Symbolic name meaning all available interfaces
   PORT = 56464              # Arbitrary non-privileged port
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.bind( (HOST, PORT) )

   print "Begin Listen"
   s.listen( 5 )
   s.settimeout(1)
   pool = list()
   while True:

      print "\nNew Connections?"
      try:
         conn, addr = s.accept()
      except( socket.timeout ):
         pass
      else:
         print 'Connected by', addr
         pool.append( Connection( conn, addr ) )
     
      for idx,val in enumerate( pool ):
         print "Check",val
         try:
            val.Recv( )
         except( socket.error ):
            pass
         if( val.Data ):
            print " Got:",val.Data
         else:
            if( val.Stale( 5 ) ):
               print " TO!"
               print " Removed!",val
               print " Age:",val.Age()
               print val.Stale( 5 )
               del pool[idx]
         val.Send( val.Data )