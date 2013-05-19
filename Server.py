# Normal Modules
import atexit
import logging
import math
import os
import Queue
import socket
import sys
import threading

# Import Third Party Modules
import pygame

# Import Custom Modules
from obj.Connection import ConnectionThread

def Main( ):
   print "Begin Main()"

   # <<<Setup Logging>>>
   
   # Create a logging class
   logger = logging.getLogger( 'log' )
   logger.setLevel( logging.DEBUG )
   fh = logging.FileHandler( 'server.log' )
   fh.setLevel( logging.DEBUG )
   formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - (%(filename)s:%(module)s:%(funcName)s:%(lineno)d) - %(message)s')
   fh.setFormatter(formatter)
   logger.addHandler(fh)
   logger.info( "Main Booted" )

   # 'application' code
   # logger.debug('debug message')
   # logger.info('info message')
   # logger.warn('warn message')
   # logger.error('error message')
   # logger.critical('critical message')

   # <<<Setup PyGame>>>
   pygame.init()
   clrDict = {
      'black' :[  0,  0,  0],
      'white' :[255,255,255],
      'blue'  :[  0,  0,255],
      'green' :[  0,255,  0],
      'red'   :[255,  0,  0]
   }

   # Setup Window
   # Recommend < 1280x800 for compatibility 
   size = [1280,800]
   screen = pygame.display.set_mode(size)
   pygame.display.set_caption("Bobble Bridge")
   clock = pygame.time.Clock()

   # Setup INet Connection
   jobsQueue = Queue.Queue()
   resultsQueue = Queue.Queue()
   quitQueue = Queue.Queue()
   lockObj = None
   address = ''
   port = 56464
   serverInput = ConnectionThread( jobsQueue, resultsQueue, quitQueue, None, address, port )
   
   # Begin server thread
   serverThread = threading.Thread( target = serverInput.Run )
   atexit.register( quitQueue.put, "Quit" )
   serverThread.start()


   running = True

   while running: 
      ### PyGame Bookkeeping ###
      clock.tick(60)
      pygame.display.set_caption( "FPS=%f"%(clock.get_fps( ) ) )
        
      for event in pygame.event.get(): # User did something
         if event.type == pygame.QUIT: # If user clicked close
            running = False # Flag that we are done so we exit this loop




      ### Networking ###
      
      while( resultsQueue.qsize() ):
         print "Network has a message!"
         try:
            tmp = resultsQueue.get( False )
            print "It was:",tmp
         except ( Queue.Empty ):
            print "Queue had something, but then it didn't? Where did it go!"
            pass



      ### Simulation ###
      # Now we must handle the simulation itself. 
   quitQueue.put("End Game")
   serverThread.join( 10.0 )
   pygame.quit()


if __name__=='__main__':
   Main()