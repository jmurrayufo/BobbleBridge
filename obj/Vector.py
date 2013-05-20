import math

"""
TODO: 
   Impliment this -> http://www.fundza.com/vectors/point2line/index.html
      in example code. 
"""


class Vector2():
   """
   Vector2 is a 2D vector representation. It supports the following...
      Addition:
         Add two vectors to find the new vector they would point two. You can add an 
         int/float/long to change its magnitude.
      Subtraction:
         As with Addition.
      Multiplication:
         Two vectors being multiplied will return a Dot Product. Vectors multiplied by an
         int/float/long will be scaled.
      Division:
         This only works for vectors divided by int/float/longs. Their magnitude is scaled
         as expected. Having a vector in a divisor makes no sense.
      Left/Right Shift:
         >> and << will cause the vector to be rotated by the angle of the vector given, 
         or by the amount of an int/float/long.

      Comparisons: 
         >, <, >=, <=, == and != all work as expected with two vectors. Vectors cannot be 
         compared to ints/floats/longs ( take the abs() or magnitude of a vector to do 
         that).

      Type Cast:
         Vectors converted into int/float/long format will use only their magnitude. 

      Vector Specific Operations:
         GetXY
            Returns an ( x, y ) tuple of the Vector.

         Unit
            Return the same vector as a unit vector.

         Normalize
            Return the same vector normalized to a given amount.

         iNormalize
            Normalize the vector in place.

   """


   def __init__( self, *args, **kargs ):
      """
      Vectors can be created in 5 different declarations
      Vector2( )
         Simple vector what points to ( 0, 0 )
      Vector2( Vector2 )
         Copy constructor
      Vector2( 4, 5 )
         Numbers without keywords are assumed to be x, y locations from (0,0)
      Vector2( x = 4, y = 5 )
         Keywords x and y are assumed to be from the origin (0,0)
      Vector2( m = 5, r = 3.14159 )
         Keyword m is the magnitude, r is the radians of the vector
      Vector2( m = 10, d = 180 )
         Keyword m is the magnitude, d is the degrees of the vector (it will be saved into
            radian format)
      """
      keys = kargs.keys()
      self.Mag = 0
      self.Angle = 0
      if( len( keys ) == 0 and len( args ) == 0 ):
         self.Mag = 0
         self.Angle = 0
      elif( len( args ) and args[0].__class__.__name__ == 'Vector2' ):
         self.Mag = args[0].Mag
         self.Angle = args[0].Angle
      elif( len( keys ) == 2 and keys[0] in ['x','y'] and keys[1] in ['x','y'] ):
         x = kargs['x']
         y = kargs['y']
         self.Mag = math.sqrt( x**2 + y**2 )
         self.Angle = math.atan2( x, y )
      elif( len(args) == 2 and type(args[0]) in [int,float,long] 
         and type(args[1]) in [int,float,long]):
         x = args[0]
         y = args[1]
         self.Mag = math.sqrt( x**2 + y**2 )
         self.Angle = math.atan2( x, y )
      elif( keys[0] in ['m','r'] and keys[1] in ['m','r'] ):
         self.Mag = kargs['m']
         self.Angle = kargs['r']
      elif( keys[0] in ['m','d'] and keys[1] in ['m','d'] ):
         self.Mag = kargs['m']
         self.Angle = kargs['d']/180.0*math.pi
      else: 
         raise ValueError, "Vectors need x,y or m,r or m,d arguments."

      if( self.Angle < 0 ):
         self.Angle += math.pi*2

      if( self.Mag < 0 ):
         self.Mag *= -1
         self.Angle += math.pi

      self.Angle %= math.pi * 2


   def __str__( self ):
      if( self.Mag > 1e6 ):
         return "M: %e A: %f"%( self.Mag, self.Angle )
      return "M: %f A: %f"%( self.Mag, self.Angle )


   # This next section of functions for fills as much of 
   #  http://docs.python.org/2/reference/datamodel.html#emulating-numeric-types as 
   #  possible


   def __add__( self, V2 ):
      if( V2.__class__.__name__ == "Vector2" ):
         x1,y1 = self.GetXY()
         x2,y2 = V2.GetXY()
         return Vector2( x=x1+x2, y=y1+y2 )
      if( type( V2 ) in [int,float,long] ):
         return Vector2( m=self.Mag+V2, r=self.Angle )


   def __radd__( self, V2 ):
      return self.__add__( V2 )


   def __lshift__( self, amount ):
      """
      Rotate the vector anti-clockwise by 'amount' radians
      """
      if( amount.__class__.__name__ in ['Vector2'] ):
         return Vector2( m = self.Mag, r = self.Angle - amount.Angle )
      if( type( amount ) in [int,float,long] ):
         return Vector2( m = self.Mag, r = self.Angle - amount )


   def __rshift__( self, amount ):
      """
      Rotate the vector clockwise by 'amount' radians
      """
      if( amount.__class__.__name__ in ['Vector2'] ):
         return Vector2( m = self.Mag, r = self.Angle + amount.Angle )
      if( type( amount ) in [int,float,long] ):
         return Vector2( m = self.Mag, r = self.Angle + amount )


   def __sub__( self, V2 ):
      if( V2.__class__.__name__ == "Vector2" ):
         x1,y1 = self.GetXY()
         x2,y2 = V2.GetXY()
         return Vector2( x = x1 - x2, y = y1 - y2 )
      if( type( V2 ) in [int,float,long] ):
         return Vector2( m = self.Mag - V2, r = self.Angle )


   def __rsub__( self, V2 ):
      return self.__sub__( V2 )


   def __mul__( self, V2 ):
      """
      Dot product of two vectors, or the magnitude will be multiplied by a value
      """
      if( V2.__class__.__name__ == "Vector2" ):
         return self.Mag * V2.Mag * math.cos( self.Angle - V2.Angle )
      if( type( V2 ) in [int,float,long] ):
         return Vector2( m = self.Mag * V2, r = self.Angle )


   def __rmul__( self, V2 ):
      return self.__mul__( V2 )


   def __div__( self, V2 ):
      if( V2.__class__.__name__ == "Vector2" ):
         raise TypeError, "unsupported operand type(s) for '/' : 'Vector2' and 'Vector2'"
      if( type( V2 ) in [int,float,long] ):
         return Vector2( m = self.Mag / V2, r = self.Angle )


   """
   This list might not be needed. These functions are left unimplemented because they 
      don't seem to have a purpose for vector math. 
   TODO list:
   def __floordiv__( self, V2 ):
   def __mod__( self, V2 ):
   def __divmod__( self, V2 ):
   def __pow__( self, V2 [:, modulo])
   def __lshift__( self, V2 ):
   def __rshift__( self, V2 ):
   def __and__( self, V2 ):
   def __xor__( self, V2 ):
   def __or__( self, V2 ):
   """


   # Unary operators (+,-,~,abs())
   def __neg__( self ):
      return Vector2( m =- self.Mag, r = self.Angle )


   def __pos__( self ):
      return Vector2( m = self.Mag, r = self.Angle )


   def __abs__( self ):
      return self.Mag


   def __invert__( self ):
      return self.__neg__()


   # Comparesons ( <, <=, >, >=, ==, != )
   def __cmp__( self, V2 ):
      # Should return a negative integer if self < other, zero if self == other,
      #  a positive integer if self > other.
      if( V2.__class__.__name__ == "Vector2" ):
         if( self.Mag < V2.Mag ):
            return -1
         if( self.Mag == V2.Mag ):
            return 0
         if( self.Mag > V2.Mag ):
            return 1
      if( type( V2 ) in [int,float,long] ):
         raise TypeError, \
            "unsupported operand type(s) for > or < or ==: 'Vector2' and '%s'"%(type(V2))
      

   # Bool support
   def __nonzero__( self ):
      return self.Mag > 1e-12 # If the vector is less then 1 trillionth of a unit, 
                              #  ignore it


   # Type support (int, float, complex)
   def __complex__(self):
      return complex( self.Mag, self.Angle )


   def __int__(self):
      return int( self.Mag )


   def __long__(self):
      return long( self.Mag )


   def __float__(self):
      return float( self.Mag )


   def GetXY( self ):
      """
      Return an X,Y tuple of the vector assumed with a center of 0
      """
      return ( self.Mag * math.sin( self.Angle ), self.Mag * math.cos( self.Angle ) )


   def Unit( self ):
      return Vector2( m = 1, r = self.Angle )


   def Normalize( self, amount = 1 ):
      return self.Unit() * amount


   def iNormalize( self, amount = 1 ):
      # Normalize in place, this modifies self!
      self.Mag = amount
      return self


   def PrettyPrint( self ):
      print self.__str__()
      print "X: %5.2f Y: %5.2f" %( 
         self.Mag * math.cos( self.Angle ),
         self.Mag * math.sin( self.Angle ) 
         )

def D2R( degrees ):
   return degrees / 180. * math.pi

def RD2( radians ):
   return radians / math.pi * 180.

if __name__ == '__main__':

   print Vector2( m=1, d=0 )
   print Vector2( 0, 1 )
   print Vector2( 1, 0 )
   v1 = Vector2( m=1, d=0 )
   v2 = Vector2( m=1, d=3 )
   print v1*v2