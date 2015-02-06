from pyglet import gl
import pyglet
import math
class NPC:
	ship = pyglet.resource.image("othership.png")
	ship.anchor_x = ship.width // 2
	ship.anchor_y = ship.height // 2
	def __init__(self, x, y, world):
		self.active = True
		self.dead = False
		self.x, self.y = x, y
		
		self.entitytype ="NPC"
		
		self.world = world
		self.texture = pyglet.sprite.Sprite(NPC.ship, batch=world.batch, group=world.layers[1])
		self.collidable = False
		self.dangerous = False
		
		self.target = None # targets hitboxes
		
		self.nerve = 0.0
		self.rate = .02
		self.weapontimer = 0.0
		self.timesincecheck = 0.0
		
	def update(self, dt):
		dangers = self.world.closeentities((self.x, self.y), 24.0)
		
		dx, dy = 0.0, 0.0
		
		if dangers:
			for d in dangers:
				distx, disty = abs(d.x - self.x), abs(d.y - self.y)
				if distx < 8.0 and disty < 8.0:
					self.dead = True
					self.world.ui.getscore()
					
					self.world.spawn("smallexplosion", self.x, self.y)
					
				if distx < disty:
					#if d.angle > (3 * math.pi)/2 - (math.pi / 4) and d.angle < (3 * math.pi)/2 + (math.pi / 4):
					if d.x > self.x:
						dx -= 16.0 * ((d.x - self.x) - self.nerve * 10.0)
					else:
						dx += 16.0 * ((self.x - d.x) - self.nerve * 10.0)
				else:
			#		if d.x > self.x:
			#			dx -= 2.0 * ((d.x - self.x) - self.nerve * 10.0)
			#		else:
				#		dx += 2.0 * ((self.x - d.x) - self.nerve * 10.0)
				
					if d.y > self.y:
						dy -= 13.0 / (d.y - self.y + self.nerve)
					else:
						dy += 16.0 / (self.y - d.y + self.nerve)
				
				self.nerve += .01
		else:
			if self.nerve > 0.0:
				self.nerve *= .95
				
			if self.nerve < 1.0:
				if self.target is None or self.timesincecheck > 2.0:
					goodone = self.world.getclosesttarget(self.x)
					self.target = goodone
					self.timesincecheck = 0.0
				else:
					if self.target.y - self.y > 300:
						dy += 80.0
					if self.x < self.target.x + self.target.w / 4:
						dx += 80.0
					elif self.x > self.target.x + self.target.w / 4:
						dx -= 80.0
					
					if self.x > self.target.x and self.x < self.target.x + self.target.w:
						if self.weapontimer > self.rate:
							self.world.play("shoot1")
							self.world.add("fireball_2",self.x - 8.0,self.y,ang=math.pi/2,spd=350.0)
							self.world.add("fireball_2",self.x + 8.0,self.y,ang=math.pi/2,spd=350.0)
							self.weapontimer = 0.0
						else:
							self.weapontimer += dt
					
				
		mx, my = max(-40, min(dx, 40)), max(-40, min(dy, 40)) 
		#print mx, my
		self.x+=mx*dt
		self.y+=my*dt
		self.texture.x, self.texture.y = self.x, self.y
		self.timesincecheck += dt
	
		