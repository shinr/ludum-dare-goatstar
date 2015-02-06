from pyglet import gl

class UI:
	def __init__(self, world):
		self.score = 0
		self.world = world
		self.healthbar = 500
		
	def draw(self):
		gl.glBegin(gl.GL_QUADS)
		gl.glVertex2f(50, 50)
		gl.glVertex2f(50 + self.healthbar, 50)
		gl.glVertex2f(50 + self.healthbar, 70)
		gl.glVertex2f(50, 70)
		gl.glEnd()