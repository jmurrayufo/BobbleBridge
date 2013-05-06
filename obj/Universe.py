import random


from Sector import Sector
from Planet import Planet


class Universe( ):
   """
   Holds the sum information for the game. 
   Every World, Object, Ship, Item etc etc etc 
   A copy of this object should be everything needed to determine what is inside the game
   at a given moment in time. 

   Note: The Universe might not hold direct copies of information, and you may need to 
   search for them
   """
   def __init__( self ):
      self.Sectors = dict()

      self.Sectors[ ( 0, 0 ) ] = Sector( ( 0, 0 ) )

   def BigBang( self ):
      self.__init__()

      locTmp = ( random.uniform( -10, 10 ), random.uniform( -10, 10 ) )

      self.Sectors[(0,0)].Add( Planet( loc = locTmp ) )

      
   def Tick( self, timeStep = 1/60.0 ): 
      """
      Run one Tick of the game world. The sim expects 60 simulated fps. 
      """
      for i in self.Sectors:
         self.Sectors[i].Tick( self, timeStep )

   def Print( self, spacing=""):
      for i in self.Sectors:
         print spacing+"Sector:",i
         print self.Sectors[i].Print( spacing+" " )
