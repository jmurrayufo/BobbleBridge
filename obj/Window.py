#!/python27/python

MASTERWINDOWEXISTS = 0

class Window:
	"""
	Window(char Type)
		Initializes a Window Variable or Type
		Return Values:
			self, if the Function returns self it has initailized a window correctly. Otherwise there is a problem of some form
		Error Codes:
			1: 
				User Has Attempted to initailize a Second Master Type Window
		Type:
			'M' or 'm':
				A Master Window, only one of these can exist at a time, if the user attempts to initailize a second one the __init__()
				fucntions hould return a value of 1
			'B' or 'b':
				A Button Type Window, many of these can exist. Any Time the screen is clicked the master window should traverse
				the tree of all sub windows to detect which button was clicked. Only Windows of Type 'B' should aknowledge Clicks
	"""
	def __init__(self,Type):
		if Type == 'M' or Type == 'm':
			print "Request For Master Window Made"
			if MASTERWINDOWEXSTS = 0:
				print "The Request is Granted"
				self.Type = 'M'
				return self
			else:
				print "The Request is Denied, A Master Window Already Exists"
				return 1
		else if Type == 'B' or Type == 'B':
			print "Request for Button. \nThe Request is Granted"
			self.Type = 'B'
			return self
		else:
			print "Request For Window of Undefined Type. Initializing Window of Type: "+Type+"This Window will be unable to perform many functions"
			self.Type = Type
			return self
	def setOffsets(self, xOffset, yOffset):
		"""
		setOffsets(xOffset,yOffset):
			sets the Offset of a Subwindow from the upper left corner of the master Window
		"""
		if Type == 'M':
			print "The master Window may not have offsets"
			return
		self.xOffset = xOffset
		self.yOffset = yOffset
	def refresh(self):
		"""
		refresh()
			This function should refresh the window to reflect all of the information which has been updated since the previous refresh
		"""
		return # this Function Has not yet been written, thus the flat return statement