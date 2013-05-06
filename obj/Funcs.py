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
