import time
import socket
import cPickle

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

class DataPacket( ):
   """
   Input/Output Container. 
   """

   # Class Defines
   # Legal Connection Values are values of the first byte 
   _LEGAL_CONNECTION_VALUES = [1,2,3,4]

   def __init__( self, data, direction='in' ):
      """
      When created, a DataPacket might require more data before being completed. 
      """

      # Data input/output is kept in the same container
      self.Data = data

      # Do we have input, or output?
      self.Direction = direction

      # Any data NOT saved is kept here for return to the origin data stream
      self.Excess = str()

      # Health state of the Packet
      #  0: Unprocessed
      #  1: Healthy
      #  2: Underflow
      #  3: Healthy-Overflow
      #  4: Corrupt
      self.Health = 0

      if( direction in ['in'] and self.Health == 0 ):
         # Start a fresh data packet
         dType = ord( data[0] )
         self.Header = dType

         # Determine if we have enough to parse yet. 
         self.Len = 0
         for i in range(3,-1,-1):
            self.Len += ord(self.Data[i+1]) * 2**( 8 * (3-i) )

         if( )

         self.CheckSum = 0
         for i in data[:-1]:
            print ord(i)
            self.CheckSum += ord(i) 
         self.CheckSum %= 256

         if( self.CheckSum == )

      elif( direction in ['out'] ):
         pass


def getLenBytes( data ):
   # Calculate 4 bytes
   retVal = list( )
   data = len( data )
   tmp = 0
   for i in range( 4 ):
      mod = 2**( 8 * (i+1) )
      div = 2**( 8 * (i) )
      retVal.append( (data % mod)/div )
      data -= retVal[-1]
   tmp = str()
   for i in retVal[::-1]:
      tmp += chr(i)
   return tmp

def PrepPacket( type, data ):
   """
   Return a prepared network packet string of type comprised in data
   """
   dType = chr(type)
   data = cPickle.dumps( data ,2 )
   dLen = getLenBytes( data )
   
   print ord(dType)

   retVal = dType + dLen + data

   chksum = 0
   for i in retVal:
      chksum+= ord(i)
      chksum%=256
   retVal = retVal + chr(chksum)
   return retVal


# Place holder test code
if __name__ == '__main__':

   x = list()
   for i in range(1):
      x.append(i)

   print "PrePacket:\n",x
   print "packet proc.:"
   x = PrepPacket(1,x)
   print "PostPacket:"


   result = DataPacket( x )

   print "\n\nResults:"
   print result.Len
   print result.Header
   print result.CheckSum
   print ord(result.Data[-1])