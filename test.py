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
   tmp = str()
   for i in retVal[::-1]:
      tmp += chr(i)
   return tmp

   
x = list()
for i in range(2**16):
   x.append(i)

print "D ready"

# print x
dtype  = chr(1)
data = cPickle.dumps(x,2)
print len(data)
dLen = getLenBytes( x )

data = dtype + dLen + data

print len(data)

chksum = 0
for i in data:
   chksum+= ord(i)
   chksum%=256
print chksum

for i in dLen:
   print ord(i)