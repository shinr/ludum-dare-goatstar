import pyglet


class Hitbox:
	engine = pyglet.resource.image("engine.png")
	engine.anchor_x = engine.width // 2
	engine.anchor_y = engine.height // 2
	def __init__(self, x, y, w, h, host, texture=None):
		self.x, self.y = x, y
		self.w, self.h = w, h
		self.entitytype = "Hitbox"
		self.host = host
		
		self.texture = pyglet.sprite.Sprite(Hitbox.engine, batch=host.world.batch, group=host.world.layers[2])
		
		self.relativeposition = (host.x - x, host.y - y)
		self.active = True
		
	def update(self, dt):
		self.x = self.host.x + self.relativeposition[0]
		self.y = self.host.y + self.relativeposition[1]
		
		if self.texture:
			self.texture.x, self.texture.y = self.x, self.y
			
		dangers = self.host.world.closeentities((self.x, self.y), 32.0, enemy=True)
		
		for i in dangers:
			self.host.world.ui.hurt()
			
			i.deactivate(-1)