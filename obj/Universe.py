
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
      