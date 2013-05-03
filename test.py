import os
import pickle
import cPickle
import time

GID = 0

class Ship( ):
   def __init__( self ):
      global GID
      self.ID = GID
      GID += 1

   def Complexer( self ):
      self.complex = 4

data = dict()

data['type'] = 0xF0
data['Enemies'] = list()

for i in range(25):
   data['Enemies'].append( Ship( ) )

sT = time.time()
with open('sizetest.txt', 'w') as fp:
   pickle.dump(data,fp,1)

print time.time()-sT

with open('sizetest.txt', 'r') as fp:
   test = pickle.load(fp)

print test['type']
print test['Enemies']
print type( test['Enemies'])