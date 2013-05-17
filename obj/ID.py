
def singleton(cls):
   instances = {}
   def getinstance():
      if cls not in instances:
         instances[cls] = cls()
      return instances[cls]
   return getinstance

@singleton
class ID():
   """
   Global ID system to handle unique creation of ID's within the game
   """
   def __init__( self ):
      # Keeps track of next ID to be issued. ID's are Ints
      self.ID = 0
      # Global lookup listing of items
      self.Objs = dict()

   def NewID( self, requestor=None ):
      self.ID += 1
      if( requestor ):
         self.Objs[ self.ID - 1 ] = requestor
      return self.ID - 1

   def Register( self, obj, objID ):
      self.Objs[ objID ] = obj

   def Unregister( self, objID ):
      del self.Objs[ objID ]

   def FindID( self, IDnum ):
      return self.Objs.get( IDnum, None )

class Foo():
   def __init__( self ):
      self.x = 4
      # 'Create' an ID instance, get the new ID, and register it
      self.ID = ID().NewID( self )

   def __del__( self ):
      print "Delete!"
      pass


if __name__ == '__main__':
   # Here we are testing to prove that two examples of ID are the same 
   # object in memory!
   s1 = ID()
   s2 = ID()
   if( id( s1 ) == id ( s2 ) ):
      print "Same"
   else:
      print "Different"

   print s1.NewID()
   print s2.NewID()
   print s2.NewID()
   print s2.NewID()

   # Prove register works
   x = Foo()
   print x

   print x.ID

   print s1.FindID(4)

   del x

   print s1.FindID(4)

