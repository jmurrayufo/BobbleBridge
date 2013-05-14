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



class ConnectionThread():
   def __init__( self, jobsQ, resultsQ, quitQ, lockObj, address, port=56464 ):
      """
      Inputs:
         jobsQ
            Outgoing data transmissions to dispatch will be Queued here
         resultsQ
            Incoming data recieved is sent here after being processed as a 
            DataPacket
         quitQ
            This Queue is empty until the thread needs to be closed. 
         lockObj
            Locking object for thread protection
         address
            IP/IPv6/address of the device to connect to
         port
            Port number to be used for connections
            Default=56464
      """




class DataPacket( ):
   """
   Input/Output Container. 
   """

   # Class Defines
   # Legal Connection Values are values of the first byte 
   #  0: Unprocessed
   #     Default state, shouldn't encounter outside of __init__
   #  1: Healthy
   #     Data was processed and found to be healthy. Data is ready for interaction
   #  2: Underflow
   #     Data indicated more data is required before processing
   #  3: Healthy-Overflow
   #     Data was processed and found to be healthy, but excess data was discovered. 
   #  4: Corrupt
   #     Unrecoverable data error. Suggested that the network buffer be cleared to reset. 
   #  5: Timeout
   #     Regardless of data state, the packet has timed out sense it's creation. 
   _LEGAL_CONNECTION_VALUES = [1,2,3,4]


   def __init__( self, data, direction='in', timeout=40 ):
      """
      Process data to be parsed out, or pickled for transmission.
      data - Data to be un-pickled from network, or Object to be pickled for network 
         transfer
      direction - Must be 'in' or 'out' to represent the meaning of the data (default: 
         'in')
      timeout - Timeout in ms of the DataPacket if receiving new injected data. 
      By default data is assumed to be incoming data to be parsed out. Data may not be in
         a contiguous form, so __init__ assumes that it make be missing or have excess 
         data to work with. On return, the Health state is set. 
      """

      # Data input/output is kept in the same container
      self.Data = data

      # Do we have input, or output?
      self.Direction = direction

      # Any data NOT saved is kept here for return to the origin data stream
      self.Excess = str()

      # Health state of the Packet
      self.Health = 0

      # Placeholder value
      self.Header = None
      self.Len = None
      self.CheckSum = None
      self.TimeCreated = None

      # We have new data with no previous state of data. Try to parse this in
      if( direction in ['in'] and self.Health == 0 ):
         # Start a fresh data packet
         self.Header = ord( data[0] )

         self.TimeCreated = time.time()

         self.Timeout = timeout

         # Get the packet size
         if( self.CalcLen() == False ):
            self.Health = 2
            return

         # We can prepare the checksum now
         if( self.CalcCheckSum() == False ):
            self.Health = 4
            return

         # Check if we had too much data 
         if( self.CalcExcess() == False ):
            self.Health = 3
            # Save from the first byte after the check sum, until the end
            self.Excess = data[ 6 + self.Len:]
            return

         # Without any other reason to assume an error, we are healthy. 
         self.Health = 1

      elif( direction in ['out'] ):
         pass


   def Inject( self, data ):
      assert( self.Health == 2 ), "Attempted to inject without underflow!"

      # Grab new data into the DataPacket
      self.Data += data

      if( time.time() - self.TimeCreated > self.Timeout/1000. ):
         self.Health = 5
         return

      # Check to see if this inject completes the packet
      if( self.CalcLen() == False ):
         self.Health = 2 # Underflow (no change!)
         return

      if( self.CalcCheckSum() == False ):
         self.Health = 4 # Corrupt data state
         return

      if( self.CalcExcess() == False ):
         self.Health = 3
         # Save from the first byte after the check sum, until the end
         self.Excess = data[ self.Len + 6: ]
         return

      self.Health = 1


   def CalcLen( self ):
      # Attempt to calculate the length of the data packet
      # Get the packet size
      if( len( self.Data ) < 5 ):
         return False

      self.Len = 0
      for i in range(3,-1,-1):
         self.Len += ord(self.Data[i+1]) * 2**( 8 * (3-i) )

      if( self.Len > len( self.Data ) - 6 ):
         self.Health = 2 # We are currently in an underflow state
         return False
      return True


   def CalcCheckSum( self ):
      # Attempt to calculate the checksum.

      # Compare the calculated check sum to the one in the data steam. This CANNOT be 
      #  wrong or there was data corruption! We have 5 bytes of header, plus the data 
      #  to get past. This operation SHOUD be index safe given the above checks in 
      #  length.
      self.CheckSum = 0
      for i in self.Data[:5 + self.Len]:
         self.CheckSum += ord(i) 
      self.CheckSum %= 256

      if( self.CheckSum != ord( self.Data[ 5 + self.Len ] ) ):
         return False
      return True
      

   def CalcExcess( self ):
      # Check if we had too much data 
      if( self.Len < len( self.Data ) - 6 ):
         return False
      return True


   def TakeExcess( self ):
      # Return any current excess, then set to healthy state
      self.Health = 1
      return self.Excess



def getLenBytes( data ):
   # Calculate 4 bytes
   retVal = list( )
   data = len( data )
   tmp = 0
   for i in range( 4 ):
      mod = 2**( 8 * (i+1) )
      div = 2**( 8 * (i) )
      retVal.append( (data % mod) / div )
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

   retVal = dType + dLen + data

   chksum = 0
   for i in retVal:
      chksum+= ord(i)
      chksum%=256
   retVal = retVal + chr(chksum)
   return retVal



# Place holder test code
if __name__ == '__main__':

   d = list()
   for i in range(10):
      d.append(i)

   print "PrePacket:"
   print "  Input:"
   print "  ",d
   print "  Packet Process..."
   x = PrepPacket(1,d)
   y = PrepPacket(1,d)
   print "\nPostPacket:"

   result = DataPacket( x[:-2] )
   print "\nInjection..."
   result.Inject( x[-2:] )

   print "\n\nResults:"
   print result.Health
