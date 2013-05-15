import obj.Connection as Connection
import threading
import Queue

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
   print "Interrupt!"
   Quitter.put("Quittin Time...")
   x.join()
   print "fin!"
   raise

Quitter.put("Quittin Time...")
x.join()

