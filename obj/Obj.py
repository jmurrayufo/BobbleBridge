

class Obj( ):
   def __init__( self, *args, **kargs):
      """
      Object storage class. Every "Thing" in the world will be derived from this class. 
      """

      # Unique ID
      self.ID = None

      # Name (Not guaranteed to be unique)
      self.Name = "DEFAULT"

      loc = kargs.get('loc',(0,0))
      # X location in the universe (in meters)
      self.X = float( loc[ 0 ] )

      # Y location in the universe (in meters)
      self.Y = float( loc[ 1 ] )

      # X velocity in reference to the universe (in meters)      
      self.VX = float()

      # Y velocity in reference to the universe (in meters)
      self.VY = float()

      # Mass of the object in Kg
      self.Mass = float()

      # Radial size of the object in meters (collision detection)
      self.Size = float()

      # Compass heading the object is facing towards
      self.Direction = float()

      # Sprite to use if it exists, this might also be overload to contain a shape
      self.Sprite = None

   def __str__( self ):
      return self.Name