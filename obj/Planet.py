from Obj import Obj

class Planet( Obj ):
   """
   All Objects (Suns, Planets, Plutoids, Asteroids) will be a 'Planet' as far as the game
   engine is concerned. 
   """
   def __init__( self, *args, **kwargs ):
      Obj.__init__( self, *args, **kwargs )
