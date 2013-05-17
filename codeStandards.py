# This file will put forth examples of how we will code the project. 

## 
# Example file

# ***DOXYGEN***
# Doxygen will provide a means of marking up code for automatic documentation. 
# To start a doxygen comment, the block cannot use """ style code blocks. You 
# need to use a ## to begin the comments, then keep the block continuous. 
# Examples if this style of code can be seen throughout this section. 
#
# Once in a Doxygen comment, you can use special markup to help make the final
# documentation result easier to read. Many functions will use few (If any!) of 
# these markup functions. Here are some good ones to try to use. 
# \bug
# \note
# \param
# \pre
# \remark
# \return
# \throw
# \throws
# \todo
# \warning
# 
# This list is not considered to be definitive or mandatory, merely a suggestion
# For a full listing, see 
# http://www.stack.nl/~dimitri/doxygen/manual/commands.html

# Classes:
class Foo():
   """
   Classes have doc strings!
   """

   def __init__( self, a, b, c=True ):
      """Constructors ALSO have doc strings!
      """
      ##
      # \param[in] a The first argument of the function
      # \param[in] b The second argument of the function
      # \param[in] c The third argument of the function
      # 
      # \return Return a Foo object
      #
      # Note that return notes aren't needed in a lot of places
      self.a=a
      self.b=b
      self.c=c

   def Bar( self, zug ):
      ##
      # \param[in] zug Amount to be squared
      #
      # \return zug ^ 2
      #
      # \note zub must be a square-able object
      #
      #
      return zug * zug


