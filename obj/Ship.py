
class Ship( ):
   def __init__( self ):
      self.ID = 0
      
      self.Name = 'DEFAULT'

      # AI event driven actions will be stored here. 
      self.Action = None

      # Event driven orders will be kept here
      self.Orders = None

      # Fleet of ship (if there is one)
      self.Fleet = None

      # We will keep four basic dicts to determine all related stats of the given ship.

      # Systems cover all basic functions of the ship (Engine, Sensors, Life Support etc etc)
      self.Systems = dict()

      # Weapons cover all offensive damage dealing weapons the ship has on board and equipped. 
      self.Weapons = dict()

      # Shields covers the 4 groups of shields, their status, and their frequencies
      self.Shields = dict()

      # Hull represents the physical state of the ship. Several components will be kept here.
      self.Hull = dict()
