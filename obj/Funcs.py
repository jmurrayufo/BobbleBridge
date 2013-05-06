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

def PrepPacket( type, data ):
   """
   Return a prepared network packet string of type comprised in data
   """
   dType = chr(type)
   data = cPickle.dumps(x,2)
   dLen = getLenBytes( x )
   
   data = dType + dLen + data

   chksum = 0
   for i in data:
      chksum+= ord(i)
      chksum%=256
   data = data + chr(chksum)
   return data

if __name__ == "__main__":
   x=list()
   for i in range(2508):
      x.append(0)

   x = PrepPacket(1,x)

   print len(x)
