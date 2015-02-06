from npc import NPC
from entity import Entity
from player import Player
from pyglet import gl
import math
from pyglet import resource
from pyglet import media
from pyglet.window import key
from pyglet import graphics
import pyglet
from potato import Potato
from uisys import UI
import sys, random
# knight, spaceship, ???

class World:
	explo = pyglet.resource.media("explo.wav")
	s1 = pyglet.resource.media("shoot.wav")
	s2 = pyglet.resource.media("shoot2.wav")
	s3 = pyglet.resource.media("shoot3.wav")
	def __init__(self, number):
		self.keysdown = []
		self.controllable = False
		self.entities = []
		self.level = number
		self.musicres = [[resource.media('epikboss_INTRO.ogg'),resource.media('epikboss_loop.wav')]]
		self.musicplayer = media.Player()
		
		self.batch = graphics.Batch()
		self.expsfx = media.Player()
		self.expsfx.queue(World.explo)
		self.expsfx.eos_action = "pause"
		
		self.s1sfx = media.Player()
		self.s1sfx.queue(World.s1)
		self.s1sfx.eos_action = "pause"
		
		self.s2sfx = media.Player()
		self.s2sfx.queue(World.s2)
		self.s2sfx.eos_action = "pause"
		
		self.s3sfx = media.Player()
		self.s3sfx.queue(World.s3)
		self.s3sfx.eos_action = "pause"
		
		self.layers = (pyglet.graphics.OrderedGroup(0), 
		pyglet.graphics.OrderedGroup(1),
		pyglet.graphics.OrderedGroup(2),
		pyglet.graphics.OrderedGroup(3),
		pyglet.graphics.OrderedGroup(4))
		
		self.ui = UI(self)
		
		
	
	def intro(self, dt):
		self.player.texture.opacity += 12
		for i in self.player.hitboxes:
			i.texture.opacity += 12
			
		if self.player.texture.opacity > 249:
			self.player.texture.opacity = 255
			pyglet.clock.unschedule(self.intro)
			self.controllable = True
	def spawn(self, thingtype, x, y, **parameters):
		if thingtype == "smallexplosion":
			self.add("smallexplosion", x, y)
		
	def add(self, entitytype, x, y, **parameters):
		if entitytype == "knight":
			self.entities.append(NPC(x, y, self))
			self.npc = self.entities[-1]
		elif entitytype == "fireball" or entitytype == "fireball_2":
			
			ang = math.atan2(y-self.npc.y, x-self.npc.x)
			spd = 70.0
			
			if 'ang' in parameters:
				ang = parameters['ang']
			
			if 'spd' in parameters:
				spd = parameters['spd']
			
			if entitytype == "fireball":
				self.entities.append(Entity(self, "projectile", x, y, angle=ang, speed=spd))
			if entitytype == "fireball_2":
				self.entities.append(Entity(self, "eprojectile", x, y, angle=ang, speed=spd))
		elif entitytype == "geometry":
			self.entities.append(Entity(self, "geometry", x, y, dimensions=(parameters["w"],parameters["h"])))
		elif entitytype == "player":
			self.entities.append(Player(self, x, y, "spaceship"))
			self.player = self.entities[-1]
		elif entitytype == "potato":
			self.entities.append(Potato(self))
		elif entitytype == "smallexplosion":
			self.entities.append(Entity(self, "smallexplosion", x, y))
	
	def init(self):
		self.musicplayer.queue(self.musicres[self.level][0])
		self.musicplayer.play()
		self.musicplayer.queue(self.musicres[self.level][1])
		pyglet.clock.schedule_interval(self.intro, 1.0)
		
	def handleinput(self, button, release=False):
		if not self.controllable: 
			return 
		if release and button in self.keysdown:
			self.keysdown.remove(button)
			if button == key.Z:
				self.player.stopfire(0)
			if button == key.X:
				self.player.stopfire(1)
			if button == key.C:
				self.player.stopfire(2)
			if button == key.LEFT:
				self.player.setmove(x=60.0)
			if button == key.RIGHT:
				self.player.setmove(x=-60.0)
			if button == key.UP:
				self.player.setmove(y=-60.0)
			if button==key.DOWN:
				self.player.setmove(y=60.0)
		elif not release:
			self.keysdown.append(button)
			if button == key.Z:
				self.player.fire(0)
			if button == key.X:
				self.player.fire(1)
			if button == key.C:
				self.player.fire(2)
			if button == key.LEFT:
				self.player.setmove(x=-60.0)
			elif button == key.RIGHT:
				self.player.setmove(x=60.0)
			if button == key.UP:
				self.player.setmove(y=60.0)
			elif button == key.DOWN:
				self.player.setmove(y=-60.0)
	
	def play(self, sound):
		if sound == "explosion":
			self.expsfx.seek(0)
			self.expsfx.play()
		elif sound == "shoot1":
			self.s1sfx.seek(0)
			self.s1sfx.play()	
		elif sound == "shoot2":
			self.s2sfx.seek(0)
			self.s2sfx.play()
		elif sound == "shoot3":
			self.s3sfx.seek(0)
			self.s3sfx.play()
			
			
	def getclosesttarget(self, x):
		candidate = None
		cdist = 0
		good = []
		for hb in self.player.hitboxes:
			if hb.active:
				if not candidate:
					candidate = hb
					cdist = hb.x - x
				else:
					if abs(hb.x - x) < abs(cdist):
						cdist = hb.x - x
						candidate = hb
		
		return candidate
	
	def shutdown(self, tick):
		pyglet.app.exit()
		sys.exit()
	
	def playerexplosion(self, tick):
		self.spawn("smallexplosion", random.randint(int(self.player.x) - 256, int(self.player.x + 256)),
			random.randint(int(self.player.y) - 64, int(self.player.y) + 64))
	
	def losecondition(self):
		self.controllable = False
		self.ui.showfinal()
		pyglet.clock.schedule_interval(self.playerexplosion, .4)
		pyglet.clock.schedule_once(self.shutdown, 5.0)
	
	def update(self, dt):
		if self.musicplayer.source == self.musicres[self.level][1] and not self.musicplayer.eos_action == 'loop':
			self.musicplayer.eos_action = 'loop'
	
		for e in self.entities:
			if self.controllable:
				e.update(dt)
			else:
				if not e.entitytype == "NPC":
					e.update(dt)
			
		for e in [todel for todel in self.entities if todel.active == False]:
			self.entities.remove(e)
			
		if self.npc.dead:
			# explosions
			self.entities.remove(self.npc)
			
			self.entities.append(NPC(random.randint(0, 600), -10, self))
			self.npc = self.entities[-1]
			
	def collide(self, entity):
		for c in [e for e in self.entities if e.collidable and not e == entity]:
			if entity.x > c.x:
				pass
			
	def closeentities(self, pos, dist, enemy=False):
		if enemy:
			dangers = [lc for lc in self.entities if lc.entitytype == "eprojectile" and abs(lc.x - pos[0]) < dist and abs(lc.y - pos[1]) < dist]
		else:
			dangers = [lc for lc in self.entities if lc.collidable and lc.dangerous and abs(lc.x - pos[0]) < dist and abs(lc.y - pos[1]) < dist]
		
		return dangers
			
			
	def render(self):
		self.batch.draw()
		self.ui.render()
		#for e in self.entities:
		#	e.render()
		
			