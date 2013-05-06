import cPickle


def getLenBytes( data ):
   # Calculate 4 bytes
   retVal = list()
   data = len(data)
   tmp = 0
   for i in range(4):
      mod = 2**( 8 * (i+1) )
      div = 2**( 8 * (i) )
      retVal.append( (data % mod)/div )
      data -= retVal[-1]
   return retVal[::-1]

   
x = list()
for i in range(2**24-1):
   x.append(i)

print "D ready"

# print x
dtype  = chr(1)
data = cPickle.dumps(x,2)
print len(data)
dLen = getLenBytes( x )

print dLen
print 2**24-1