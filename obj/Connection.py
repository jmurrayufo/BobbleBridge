import collections
import cPickle
import Queue
import socket
import threading
import time

class Connection():
   """
   Connection provides a wrapper to help handle a lot of repeat connection code
      between the server and the client. 
   """
   def __init__( self, address='', port=56464, bind=True, connection=None ):
      ##
      # Constructor
      # \param address IP/URL of the server to connect to (default of '')
      # \param port Port number (default of 56464)
      # \param bind Sets this connect to bind to an interface, rather then connecting to a 
      # remote server
      # \param connection A given active socket connection to copy onto this object. Will 
      # not attempt to make a new connection if this exists. 
      self.Address = address
      self.Port = port
      self.Bind = bind

      self.FirstHeard = time.time()
      self.LastHeard = time.time()

      self.Data = ''

      self.Packets = collections.deque()
      self.In = 0
      self.Out = 0

      self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      if( connection ):
         self.Socket = connection

      else:
         if( self.Bind ):
            self.Socket.bind( ( self.Address, self.Port ) )
            self.Socket.listen( 5 )
         else:
            self.Socket.connect( ( self.Address, self.Port ) )
         self.Socket.settimeout( 0 )


   def __del__( self ):
      # Lets be nice and try to close the connection when we are deleted
      self.Socket.close()


   def __str__( self ):
      return "%s:%d"%( self.Address, self.Port )


   def __repr__( self ):
      return self.__str__( )


   def Recv( self, size = 4096 ):
      """
      Attempt to receive a given amount of data from the connection.
      """
      ##
      # \param size Number of bytes to attempt to pull from the connection.
      self.Data = str()
      try:
         self.Data = self.Socket.recv( size )
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
      """
      Check if the connection has received a full Data Packet that is read for reading. 
      """
      ##
      # \return True if at least one packet exists, False otherwise. 
      if( len( self.Packets ) == 0 ):
         return False

      # Is the top of the packet deque healthy?
      if( self.Packets[0].Health in [ 1, 3 ] ):
         return True

      # Nothing to get yet!
      else:
         return False


   def GetPacket( self ):
      """
      Return the oldest healthy packet from the Connection. Will begin to break open 
      packets with excess data if needed to slurp up data. 
      """
      ##
      # \return Oldest healthy packet, or None if none exist
      # Do we have ANY packets?
      if( len( self.Packets ) == 0 ):
         return None

      # Is the top of the packet deque healthy?
      if( self.Packets[0].Health == 1 ):
         return self.Packets.popleft( )

      # Do we need to slurp up excess then return an overflowed packet?
      elif( self.Packets[0].Health == 3):
         extra = self.Packets[0].TakeExcess( )
         self.Packets.append( DataPacket( extra ) )
         return self.Packets.popleft( )

      elif( self.Packets[0].Health in [ 4, 5 ] ):
         self.Flush( )
         return None

      # Nothing to get yet!
      else:
         return None


   def Send( self, data ):
      """
      Attempt to send a given block of data to the established connection. If the data is
      not already in the DataPacket form, it will be converted into it before transmission
      """
      ##
      # \param data Information to be transmitted to the connection
      # \todo This needs to check if this is raw data, or a DataPacket. Both 
      #  should be handled.
      if( data.__class__.__name__ == 'DataPacket' ):
         data = data.Data
      else:
         data = DataPacket( data, direction = 'out' ).Data
      retries = 0
      while True:
         try:
            self.Socket.sendall( data )
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


   def Accept( self ):
      """
      Attempts to accept any new connections. This makes zero sense to non-Bind connections
      """
      ## 
      if( self.Bind ):
         try:
            conn, addr = self.Socket.accept()
            return Connection( address = addr[0], port = addr[1], bind = False, connection = conn )
         except( socket.timeout, socket.error ):
            pass
         return None
      else: 
         raise socket.error


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
            self.Data = self.Socket.recv( 4096 )
         except( socket.error ):
            break


   def Heal( self, cause=None ):
      """
      Attempt to correct errors in the connection
      """
      ##
      # \param cause Placeholder, Ignored. Will eventually allow Heal to respond correctly 
      # to the issue. 
      self.Socket.close()
      self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      try:
         self.Socket.connect( ( self.Address, self.Port) )
         self.Socket.settimeout( 0 )
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
      self.Socket.close()



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
      if( Ctype == 'server' ):
         self.Connection = Connection( address, port, True )
      elif( Ctype == 'client' ):
         self.Connection = Connection( address, port, False )
      self.Ctype = Ctype

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
               tmp = self.Connection.Accept()
               # TODO: Replace this print line with a logging call
               if( tmp ):
                  print 'Connected by', tmp
                  pool.append( tmp )
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

      elif( self.Ctype == 'client' ):

         # Prime the heartbeat          
         heartbeat = 5
         lastHeartBeat = time.time() - heartbeat 

         print "Connected!"
         while True:

            tmpDiff = time.time() - lastFrame
            if( tmpDiff < 1/float(RunFrameRate) ):
               time.sleep( 1/float(RunFrameRate) - tmpDiff )
            lastFrame = time.time()
            try:
               self.Connection.Recv( )
            except( socket.error ):
               raise
            
            while( self.Connection.HasPacket() ):
               self.resultsQ.put( self.Connection.GetPacket( ) )
            
            # TODO: Adjust this section to handle sending errors like bellow
            while( self.JobsQ.empty() == False ):
               tmp = self.JobsQ.get()
               # self.Connection.Send( DataPacket( tmp, direction='out' ) )
               self.Connection.Send( tmp )


            if( self.QuitQ.empty() == False ):
               self.Connection.Close()
               return

            if( time.time() - lastHeartBeat > heartbeat ):
               print "Thump!"
               self.Connection.Send( "Thump!" ) 
               lastHeartBeat = time.time()

            if( self.Connection.Stale( ) ):
               # TODO: This section should be a log, not a print
               print "\nCheck",self.Connection
               print " Connection timed Out"
               print " Removed!",self.Connection
               print " Age:",self.Connection.GetAge()
               print " In:",self.Connection.In
               print " Out:",self.Connection.Out
               print " Btyes/s:",(self.Connection.In + self.Connection.Out)/self.Connection.GetAge()
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
