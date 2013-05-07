from Obj import Obj

class Station( Obj ):
   def __init__( self, *args, **kwargs ):
      Obj.__init__( self, *args, **kwargs )

      # Eventuall goal here, is to represent the Equipment, hull state, trade goods etc
      #  that a station might offer. 