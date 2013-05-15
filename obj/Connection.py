import collections
import cPickle
import Queue
import socket
import threading
import time

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
      self.Data = ''
      self.Packets = collections.deque()
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
         # Check if we have ANY packets
         if( len( self.Packets ) ):
            # We have packets of data, process them into the deque 

            # Check for timed-out packets and corrupt packets
            if( self.Packets[-1].Health in [ 5, 4 ] ):
               # We have a corrupt state, this connection needs to be flushed
               self.Flush()
               return

            # Check for overflow
            elif( self.Packets[-1].Health == 3 ):
               extra = self.Packets[-1].TakeExcess()
               self.Packets.append( DataPacket( extra + self.Data ) )
            # Check for underflow
            elif( self.Packets[-1].Health == 2 ):
               self.Packets[-1].Inject( self.Data )
            # Check for happy healthy state
            elif( self.Packets[-1].Health == 1 ):
               self.Packets.append( DataPacket( self.Data ) )
         else: 
            # New data, start the deque
            self.Packets.append( DataPacket( self.Data ) )
         
         # Data is now processed, blank it out
         self.Data = ''


   def HasPacket( self ):
      if( len( self.Packets ) == 0 ):
         return False

      # Is the top of the packet deque healthy?
      if( self.Packets[0].Health in [ 1, 3 ] ):
         return True

      # Nothing to get yet!
      else:
         return False


   def GetPacket( self ):
      # Do we have ANY packets?
      if( len( self.Packets ) == 0 ):
         return None

      # Is the top of the packet deque healthy?
      if( self.Packets[0].Health == 1 ):
         return self.Packets.popleft()

      # Do we need to slurp up excess then return an overflowed packet?
      elif( self.Packets[0].Health == 3):
         extra = self.Packets[0].TakeExcess()
         self.Packets.append( DataPacket( extra ) )
         return self.Packets.popleft()

      # Nothing to get yet!
      else:
         return None


   def Send( self, data ):
      # TODO: This needs to check if this is raw data, or a DataPacket. Both 
      #  should be handled.
      if( data.__class__.__name__ == 'DataPacket' ):
         data = data.Data
      else:
         if( data[0] == 'E' ):
            data = DataPacket( data, direction = 'out' ).Data
            data = data[0:4] + '\xFF' + data[5:]
         else:
            data = DataPacket( data, direction = 'out' ).Data
      retries = 0
      while True:
         try:
            self.Conn.sendall( data )
            self.Out += len( data )
            self.LastHeard = time.time()
            break
         except ( socket.error ) as e:
            print "Waiting %d seconds"%( retries )
            time.sleep(retries)
            retries += 1
            if( retries > 5 ):
               raise
            # TODO: This call should be moved to the Thread, so that we can
            #  catch interrupts while we run. 
            self.Heal()



   def Flush( self ):
      print "Flush!"
      for i in self.Packets:
         print i
         print i.Health
         print i.Header
         print i.Len
         print i.CheckSum
         print i.TimeCreated

      self.Packets = collections.deque()
      self.Data = ''
      while True:
         try:
            self.Data = self.Conn.recv( 4096 )
         except( socket.error ):
            break


   def Heal( self, cause=None ):
      """
      For some reason the connection shows as having a problem. Lets try to heal it!
      """
      self.Conn.close()
      self.Conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      try:
         self.Conn.connect( self.Addr )
         self.Conn.settimeout( 0 )
      except ( socket.error ) as e2:
         if( e2[0] == 10061 ):
            print "Packet Refused"
         else:
            raise



   def GetAge( self ):
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
   def __init__( self, jobsQ, resultsQ, quitQ, lockObj, address, port=56464, Ctype='server' ):
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
         Ctype
            This can be 'server' or 'client' depending on the style of thread needed
      """
      self.JobsQ = jobsQ
      self.ResultsQ = resultsQ
      self.QuitQ = quitQ
      self.LockObj = lockObj
      # Run basic setup of the ConnectionThread
      self.Host = address # Symbolic name meaning all available interfaces
      self.Port = port
      self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      if( Ctype == 'server' ):
         self.s.bind( ( self.Host, self.Port ) )
         self.s.listen( 5 )
      elif( Ctype == 'client' ):
         self.s.connect( ( self.Host, self.Port ) )
      self.Ctype = Ctype
      self.s.settimeout( 0 )

      # The Pool holds the set of connections we care about
      self.Pool = list()

   def Run( self ):
      # Infinite loop of execution
      RunFrameRate = 60
      lastFrame = time.time()
      if( self.Ctype == 'server' ):  
         pool = list()
         while True:
            tmpDiff = time.time() - lastFrame
            if( tmpDiff < 1/float(RunFrameRate) ):
               time.sleep( 1/float(RunFrameRate) - tmpDiff )
            lastFrame = time.time()
            # Check for new connections to add to the pool
            try:
               conn, addr = self.s.accept()
               # TODO: Replace this print line with a logging call
               print 'Connected by', addr
               pool.append( Connection( conn, addr ) )
            except( socket.timeout, socket.error ):
               # No connections were received, move on
               pass
            
            # Handle incoming client requests
            for idx,val in enumerate( pool ):
               # Try to receive data
               # TODO: This try-except might be handled by the Connection class
               #  already. Look into this and remove if it isn't needed
               try:
                  val.Recv( )
               except( socket.error ):
                  pass
               while( val.HasPacket() ):
                  tmp = val.GetPacket( )
                  print tmp
                  print tmp.Open()
                  self.ResultsQ.put( tmp )
                  # print "Check",val
                  # print " Got:",val.Data
               if( val.Stale( ) ):
                  # TODO: This section should be a log, not a print
                  print "\nCheck",val
                  print " Connection timed Out"
                  print " Removed!",val
                  print " Age:",val.GetAge()
                  print " In:",val.In
                  print " Out:",val.Out
                  print " Btyes/s:",(val.In + val.Out)/val.GetAge()
                  del pool[idx]
               # Outgoing data must be pulled from the jobsQ, this might require
               #  filtering based on several connections
               # try:
               #    val.Send( val.Data )
               # except socket.error as e :
               #    # Work needs to be done here to handle a larger range of error codes. 
               #    if( e.errno == 10035 ):
               #       pass
               #    else:
               #       print " Cannot send! Delete!"
               #       print e,
               #       del pool[idx]

      elif( self.Ctype == 'client' ):

         # Prime the heartbeat          
         heartbeat = 5
         lastHeartBeat = time.time() - heartbeat 

         # Connect to server
         server = Connection( self.s, ( self.Host, self.Port ) )
         print "Connected!"
         while True:

            tmpDiff = time.time() - lastFrame
            if( tmpDiff < 1/float(RunFrameRate) ):
               time.sleep( 1/float(RunFrameRate) - tmpDiff )
            lastFrame = time.time()
            try:
               server.Recv( )
            except( socket.error ):
               raise
            
            while( server.HasPacket() ):
               self.resultsQ.put( server.GetPacket( ) )
            
            # TODO: Adjust this section to handle sending errors like bellow
            while( self.JobsQ.empty() == False ):
               tmp = self.JobsQ.get()
               # server.Send( DataPacket( tmp, direction='out' ) )
               server.Send( tmp )


            if( self.QuitQ.empty() == False ):
               server.Close()
               return

            if( time.time() - lastHeartBeat > heartbeat ):
               print "Thump!"
               server.Send( "Thump!" ) 
               lastHeartBeat = time.time()

            if( server.Stale( ) ):
               # TODO: This section should be a log, not a print
               print "\nCheck",server
               print " Connection timed Out"
               print " Removed!",server
               print " Age:",server.GetAge()
               print " In:",server.In
               print " Out:",server.Out
               print " Btyes/s:",(server.In + server.Out)/server.GetAge()
               return




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


   def __init__( self, data, direction='in', timeout=1000 ):
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
         # TODO: Check the health of the resultant packet
         self.Data = PrepPacket( 0, self.Data )
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


   def Open( self ):
      if( self.Health == 1 ):
         return cPickle.loads( self.Data[5:-1] )

      else:
         return None


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
   data = cPickle.dumps( data, 2 )
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

   Jobs = Queue.Queue()
   Results = Queue.Queue()
   Quitter = Queue.Queue()
   Locker = threading.Lock()


   x = ConnectionThread(
      Jobs, 
      Results,
      Quitter, 
      Locker, 
      '', 
      port=56464, 
      Ctype='server' 
      )
   x.Run()
