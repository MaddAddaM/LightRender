class LightPosition:
	POSITION_GRID_WIDTH = 1000
	POSITION_GRID_HEIGHT = 1000

	def __init__(self, index, x, y):
		self.index = index
		self.x = x
		self.y = y

	# I represent positions on a grid of fixed size, but you need to know where I am on your grid
	def GetRelativeX(self, widthRelativeTo):
		return round(self.x * (widthRelativeTo / float(LightPosition.POSITION_GRID_WIDTH)))

	def GetRelativeY(self, heightRelativeTo):
		return round(self.y * (heightRelativeTo / float(LightPosition.POSITION_GRID_HEIGHT)))