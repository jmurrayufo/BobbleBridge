

def DistanceConv( data, have, want ):
   coversionTbl = {
   # Metric
   'm':1000.,
   'km':1,
   # Astro
   'ly':1.057e-13,
   'pc':3.241e-14,
   'au':6.685e-09,
   'lm':5.559e-08,
   'ls':3.336e-06,
   # Stupid
   'mi':0.6214,
   'ft':3281.,
   'yd':1094.,
   'in':39370.1
   }
   have = have.lower()
   want = want.lower()

   assert( have in coversionTbl.keys( ) ),"Have value %s not in table"%(have)
   assert( want in coversionTbl.keys( ) ),"Want value %s not in table"%(want)

   # Covert from 'have' to 'want'
   data *= coversionTbl['km']/coversionTbl[have]
   print "km:",data
   data *= coversionTbl[want]

   return data

print DistanceConv(100,'au','m')