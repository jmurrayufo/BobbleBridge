import obj.Connection as Connection
import threading
import Queue
import logging

logger = logging.getLogger( 'log' )
logger.setLevel( logging.DEBUG )
fh = logging.FileHandler( 'client.log' )
fh.setLevel( logging.DEBUG )
formatter = logging.Formatter('%(asctime)s - %(levelname)s - (%(filename)s:%(module)s:%(funcName)s:%(lineno)d) - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info( "Main Booted" )
for i in range(10):
   logger.info("***************")

Jobs = Queue.Queue()
Results = Queue.Queue()
Quitter = Queue.Queue()
Locker = threading.Lock()


x = Connection.ConnectionThread(
      Jobs, 
      Results,
      Quitter, 
      Locker, 
      '127.0.0.1', 
      port=56464, 
      Ctype='client' 
   )  

x = threading.Thread( target = x.Run )

x.start()
try:
   for i in range( 10 ):
      Jobs.put( raw_input(">") )
except ( KeyboardInterrupt ):
   logger.error( "Keyboard Termination!" ) 
   print "Interrupt!"
   Quitter.put("Quittin Time...")
   logger.debug( "Begin join call" )
   x.join()
   logger.debug( "Finished join call" )
   print "fin!"
   raise

Quitter.put("Quittin Time...")
logger.info( "End Program" )
logger.debug( "Begin join call" )
x.join( 10.0 )
logger.debug( "Finished join call" )

