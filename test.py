import threading
import time

def Foo( lockObj=None ):
   myThread = threading.current_thread()
   for i in range(100):
      lockObj.acquire() 
      print i
      lockObj.release()


lockBox = threading.Lock()
for i in range(5):
   threading.Thread( target=Foo, kwargs=({'lockObj':lockBox}) ).start()
