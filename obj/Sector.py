from Ship import Ship
from Planet import Planet


class Sector( ): 
   """
   Universe is made up of sectors, each sector contains links to things that are inside 
   it. The game will keep 9 sectors loaded around the players at a time. This class exists
   primarily to support the transfer of small packets of information across the network. 
   """
   def __init__( self, loc = (0,0) ):
      self.X = loc[0]
      self.Y = loc[1]

      self.Ships = list()
      self.Planets = list()

   def Tick( self, caller, timeStep = 1/60.0 ):
      pass

   def Add( self, object ):
      if( object.__class__.__name__ == 'Planet' ):
         self.Planets.append( object )

   def Print( self, spacing=""):
      """
      Print pretty output to provide debug information about a given sector
      """
      for i in self.Ships:
         print spacing+"Ship:",i

      for i in self.Planets:
         print spacing+"Planet:",i
         print " "+spacing+"x:",i.X
         print " "+spacing+"y:",i.Y