from pyglet import gl
from hitbox import Hitbox
import pyglet
import math
class Player:
	ship = pyglet.resource.image("spaceship2.png")
	ship.anchor_x = ship.width // 2
	ship.anchor_y = ship.height // 2
	radinc = math.radians(5.0)
	def __init__(self, world, x, y, pmode):
		self.x, self.y = x, y
		self.collidable = True
		self.dangerous = False
		
		self.entitytype = "Player"
		self.active = True
		
		self.texture = pyglet.sprite.Sprite(Player.ship, batch=world.batch, group=world.layers[1])
		self.world = world
		self.hitboxes = [Hitbox(self.x-104.0, self.y+48, 64.0, 128.0, self), 
		Hitbox(self.x+104.0, self.y+48, 64.0, 128.0, self)]
		self.texture.opacity = 0.0
		for i in self.hitboxes:
			i.texture.opacity = 0.0
		
		
		if pmode == "spaceship":
			self.sx, self.sy = 0.0, 0.0
	
		self.firing = False
		self.weapon = 0
		self.angle = math.radians(270.0)
		self.rate = 1.0
		self.weapontimer = 0.0
		
	def setmove(self, x=None, y=None):
		if not x is None:
			self.sx += x
		if not y is None:
			self.sy += y
		
	def stopfire(self, weapon):
		if self.weapon == weapon:
			self.firing	= False
			self.weapontimer = 99.0
	
	def fire(self, weapon):
		if weapon == 0:
			self.firing = True
			self.angle = math.radians(270.0)
			self.weapon = 0
			self.rate = 0.22
			self.weapontimer = 0.0
		elif weapon == 1:
			self.firing = True
			self.angle = math.radians(270.0)
			self.weapon = 1
			self.rate = 0.26
			self.weapontimer = 0.0
		elif weapon == 2:
			self.firing = True
			self.angle = math.radians(300.0)
			self.weapon = 2
			self.rate = 0.5
			self.weapontimer = 0.0
			
	def update(self, dt):
		self.texture.x,self.texture.y = self.x, self.y
		for hb in self.hitboxes:
			hb.update(dt)
		if self.firing:
			if self.weapontimer > self.rate:
				if self.weapon == 0:
					self.world.play("shoot1")
					rads = self.angle
					self.world.add("fireball",self.x - 198.0,self.y-90.0,ang=rads,spd=250.0)
					self.world.add("fireball",self.x + 198.0,self.y-90.0,ang=rads,spd=250.0)
					self.world.add("fireball",self.x - 238.0,self.y-90.0,ang=rads,spd=250.0)
					self.world.add("fireball",self.x + 238.0,self.y-90.0,ang=rads,spd=250.0)
					self.world.add("fireball",self.x - 56.0,self.y-98.0,ang=rads,spd=250.0)
					self.world.add("fireball",self.x + 56.0,self.y-98.0,ang=rads,spd=250.0)
				elif self.weapon == 1:
					self.world.play("shoot2")
					rads = self.angle
					self.angle += Player.radinc
					if self.angle > 2 * math.pi:
						self.angle = 0.0
					elif self.angle < 0.0:
						self.angle = 2 * math.pi
					self.world.add("fireball",self.x + 66.0,self.y+32.0,ang=rads,spd=250.0)
					self.world.add("fireball",self.x - 66.0,self.y+32.0,ang=rads,spd=250.0)
					self.world.add("fireball",self.x + 66.0,self.y+32.0,ang=rads+ math.pi/2,spd=250.0)
					self.world.add("fireball",self.x - 66.0,self.y+32.0,ang=rads+ math.pi/2,spd=250.0)
					self.world.add("fireball",self.x + 66.0,self.y+32.0,ang=rads- math.pi/2,spd=250.0)
					self.world.add("fireball",self.x - 66.0,self.y+32.0,ang=rads- math.pi/2,spd=250.0)
					self.world.add("fireball",self.x + 66.0,self.y+32.0,ang=rads- math.pi,spd=250.0)
					self.world.add("fireball",self.x - 66.0,self.y+32.0,ang=rads- math.pi,spd=250.0)
				elif self.weapon == 2:
					self.world.play("shoot3")
					rads = self.angle
					
					self.world.add("fireball",self.x - 162.0,self.y-80.0,ang=rads,spd=250.0)
					self.world.add("fireball",self.x + 162.0,self.y-80.0,ang=rads - math.pi / 3,spd=250.0)
					self.world.add("fireball",self.x - 162.0,self.y-80.0,ang=rads - Player.radinc * 2,spd=250.0)
					self.world.add("fireball",self.x + 162.0,self.y-80.0,ang=rads + Player.radinc * 2 - math.pi/3,spd=250.0)
					self.world.add("fireball",self.x - 162.0,self.y-80.0,ang=rads - Player.radinc * 4,spd=250.0)
					self.world.add("fireball",self.x + 162.0,self.y-80.0,ang=rads + Player.radinc * 4 - math.pi/3,spd=250.0)
					self.world.add("fireball",self.x - 162.0,self.y-80.0,ang=rads - Player.radinc * 6,spd=250.0)
					self.world.add("fireball",self.x + 162.0,self.y-80.0,ang=rads + Player.radinc * 6 - math.pi/3,spd=250.0)
					self.world.add("fireball",self.x - 162.0,self.y-80.0,ang=rads - Player.radinc * 8,spd=250.0)
					self.world.add("fireball",self.x + 162.0,self.y-80.0,ang=rads + Player.radinc * 8 - math.pi/3,spd=250.0)
					
				self.weapontimer = 0.0
			else:
				self.weapontimer += dt
				
		self.x, self.y = self.x + self.sx * dt, self.y + self.sy * dt
		if self.x < 200.0:
			self.x = 200.0
		elif self.x > 400.0:
			self.x = 400.0
		if self.y > 750.0:
			self.y = 750.0
		elif self.y < 550.0:
			self.y = 550.0
	def render(self):
		self.texture.draw()
		
		for hb in self.hitboxes:
			hb.render()