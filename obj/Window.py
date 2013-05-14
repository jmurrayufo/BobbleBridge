"""
Window will be used for all of the windows and visual displays in the game.

This Module Assumes that
import pygame
&
from pygame.locals import *
&
pygame.init()
Have all been asserted

Note: you can change the working directory with os.chdir( path ).
"""
class Window:
	Width  = 0
	Height = 0
	WidthOffset  = 0
	HeightOffset = 0
	def __init__(self,*args,**kargs):
		"""
		 Window()
			Creates an empty window bucket. This Window Can Be manipulated
		 Window(Window)
			Copy Constructor
		 Window(int, int)
			Two Integer Arguments will result in a window being created of width int1 and height int2
			This window will be initialized in the upper left corner of the screen
		Window(int, int, int, int)
			four integers will be treated as such Width, Height, X Offset, Y Offset
		Window("M") or Window("m")
			initializes this Window as the master window
			The master window is the window in which other windows will be drawn.	
		"""
		if self.args[1] == 'M' or self.args[1] == 'm':
			print 'Hit Master Case'
 
	def setLayer(int):
		"""
		 Set the 'Layer of the window' To the specified integer, Windows will higher integers will be given display
		 priority over lower layers.
		"""
	def draw():
		"""
			Draw the Window onto the Screen
		"""
		 
 