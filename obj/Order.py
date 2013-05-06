
class Order( ):
   """
   This class maintains orders for ships and fleets
   """

   def __init__( self ):

      """
      Given types can be:
         
         Goto
            Go to a given location. Use any means to get there
         
         Attack
            Can be a location OR an object. Locations will result in closing to the given location and then finding valuable targets. Obejcts will result in the AI ignoring all other enemies to focus fire. The may imply a goto depending on distance to target.
         
         Move-Attack
            Combination of Goto and Attack location. Will use any means to get to a given location, but will attack any enemies it finds along the way.
         
         Defend
            Can be given as a location OR an object. Locations will result in the ship standing guard at a given location until a new order arrives. Defending an object will result in the ship following its target and attacking any enemies nearby. This implies a goto. 
         Follow
            Non-hostile action, following a given target. Will ignore enemies along the way. 

         Hide
            Depart from any major traffic and attempt to avoid being found. This implies non-hostile intentions

         Explore
            Wonder into nearby unknown locations for your faction, scan for interesting things, repeat.

      """
      self.Type = None