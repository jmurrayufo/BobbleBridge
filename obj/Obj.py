from Vector import Vector2

class Obj( ):
   def __init__( self, *args, **kargs):
      """
      Object storage class. Every "Thing" in the world will be derived from this class. 
      """

      ## Unique ID
      # This should be a unique number to identify the object in the program.
      self.ID = None

      ## Name (Not guaranteed to be unique)
      self.Name = "DEFAULT"

      ## Numeric faction alliance. 
      # Special Cases:
      # * -1: All other non zero targets are enemies, including other -1's
      # * 0: Neutral (eg: planet, asteroid)
      # * 1: Players faction
      # * 2+: Positive integers represent unique factions at war with each other
      self.Faction = 0  

      loc = kargs.get( 'loc', ( 0, 0 ) )

      # Location in reference to local sector
      self.Loc = Vector2( x = loc[0], y = loc[1] )

      # Velocity of the object, kept in m/s
      self.Vel = Vector2( m=0, d=0 )

      # Mass of the object in Kg
      self.Mass = float( )

      # Radial size of the object in meters ( collision detection )
      self.Size = float( )

      # Compass heading the object is facing towards
      self.Direction = float( )

      # Sprite to use if it exists, this might also be overload to contain a shape
      self.Sprite = None

   def __str__( self ):
      return self.Name