from pyglet import gl
import pyglet
class UI:
	def __init__(self, world):
		self.score = 0
		self.world = world
		self.healthbar = 500.0
		self.dead = False
		self.labels = [pyglet.text.Label(text='score:',x=10, y=790, group=world.layers[4]),
			pyglet.text.Label(text='0', x=120, y=790, group=world.layers[4])]
		
	def hurt(self):
		if self.healthbar > 1.0:
			self.healthbar -= 1.0
		else:
			self.healthbar = 1.0
			self.world.losecondition()
		
	def getscore(self):
		self.score += 100
		self.labels[1].text = str(self.score)
		
	def showfinal(self):
		self.labels[0].text="FINAL SCORE:"
		self.labels[0].x=300
		self.labels[0].y=400
		self.labels[0].anchor_x="center"
		self.labels[0].font_size=36
		
		self.labels[1].x=300
		self.labels[1].y=348
		self.labels[1].anchor_x="center"
		self.labels[1].font_size=36
	
	def render(self):
		di = (self.healthbar / 100)
		if di < 1.0:
			di = 1.0
		
		gl.glBegin(gl.GL_QUADS)
		gl.glColor4f(1.0/di, 1.0 - 1/di, 0.0, 0.5)
		gl.glVertex2f(50, 10)
		gl.glVertex2f(50 + self.healthbar, 10)
		gl.glVertex2f(50 + self.healthbar, 20)
		gl.glVertex2f(50, 20)
		gl.glEnd()
		
		
		for item in self.labels:
			item.draw()