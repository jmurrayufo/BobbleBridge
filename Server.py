# Normal Modules
import math
import os
import socket
import sys
import threading
import Queue

# Import Third Party Modules
import pygame

# Import Custom Modules
from obj.Connection import ConnectionThread

def Main( ):
   print "Begin Main()"
   ####  Setup PyGame ####
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
   HOST = '' # Symbolic name meaning all available interfaces
   PORT = 56464
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.bind( (HOST, PORT) )
   s.listen( 5 )
   s.settimeout( 0 )
   pool = list()


   running = True

   while running: 
      ### PyGame Bookkeeping ###
      clock.tick(60)
      pygame.display.set_caption( "FPS=%f"%(clock.get_fps( ) ) )
        
      for event in pygame.event.get(): # User did something
         if event.type == pygame.QUIT: # If user clicked close
            running = False # Flag that we are done so we exit this loop




      ### Networking ###
      
      # Accept new incoming connections, Append them to our list
      try:
         conn, addr = s.accept()
         print 'Connected by', addr
         pool.append( Connection( conn, addr ) )
      except( socket.timeout, socket.error ):
         pass
      
      # Handle incoming client requests
      for idx,val in enumerate( pool ):
         # print "Check",val
         try:
            val.Recv( )
         except( socket.error ):
            pass
         if( val.Data ):
            pass
            # print "Check",val
            # print " Got:",val.Data
         else:
            if( val.Stale( 1 ) ):
               print "\nCheck",val
               print " Connection timed Out"
               print " Removed!",val
               print " Age:",val.Age()
               print " In:",val.In
               print " Out:",val.Out
               print " Btyes/s:",val.In/val.Age()
               del pool[idx]
         try:
            val.Send( val.Data )
         except socket.error as e :
            # Work needs to be done here to handle a larger range of error codes. 
            if( e.errno == 10035 ):
               pass
            else:
               print " Cannot send! Delete!"
               print e,
               del pool[idx]



      ### Simulation ###
      # Now we must handle the simulation itself. 
   pygame.quit()


if __name__=='__main__':
   Main()