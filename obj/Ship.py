from Obj import Obj

class Ship( Obj ):
   def __init__( self, *args, **kwargs ):
      Obj.__init__( self, *args, **kwargs )

      # AI event driven actions will be stored here. 
      self.Action = None

      # Event driven orders will be kept here
      self.Orders = None

      # Fleet of ship (if there is one)
      self.Fleet = None

      # Systems cover all basic functions of the ship (Engine, Sensors, Life Support etc etc)
      self.Systems = dict()

      # Weapons cover all offensive damage dealing weapons the ship has on board and equipped. 
      self.Weapons = dict()

      # Shields covers the 4 groups of shields, their status, and their frequencies
      self.Shields = dict()

      # Hull represents the physical state of the ship. Several components will be kept here.
      self.Hull = dict()

   def __str__( self ):
      return "ship"+str(self.X)