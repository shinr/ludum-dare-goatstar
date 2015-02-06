import pyglet
from world import World


class Main(pyglet.window.Window):
	logo = pyglet.resource.image("logo.png")
	info = pyglet.resource.image("info.png")
	logo.anchor_x, logo.anchor_y = logo.width // 2, logo.height // 2
	info.anchor_x, info.anchor_y = info.width // 2, info.height // 2
	coin = pyglet.resource.media("coin.wav")
	def __init__(self):
		pyglet.window.Window.__init__(self, 600, 800)
		self.info = True
		self.logo = pyglet.sprite.Sprite(Main.logo, 300, 700)
		self.info = pyglet.sprite.Sprite(Main.info, 300, 130)
		self.story = pyglet.text.Label(x=300, y=600, anchor_x="center", width = 512,multiline=True)
		self.story.text="As The Master of Intergalactic Goatoperium, Lord Francis von Vuohi, you have stood against countless enemies as you conquered the Stars to place them under your Iron Hooves.  Blood has been spilled, but for reason, for how would those pesky ingrates learn otherwise.\n\nStill, now you again stand on the battlefield.  Those pesky rebels, usually no more than an annoyance, have gathered in millions to... 'liberate' the Goatoperium.  Ha, what a laugh.\n\nUngrateful peasants.  You gave them work, a meaning, to serve their Goatomperor!  Yet they dare oppose you still, maggots.\n\nVery well.  Let them bring thousands, bring millions!  With the guns of the greatest Warship of Goatomperium, the GOATSTAR, all will be crushed and their blood shall colour the stars themselves red.  Let them cry for mercy, only to receive none.\n\n---\n\nNow you're the big guy.  Destroy as many enemy fighters as you can before you fall."
		

	def update(self, dt):
		if not self.info:
			self.world.update(dt)
		
	def on_draw(self):
		self.clear()
		
		if not self.info:
			self.world.render()
		else:
			self.logo.draw()
			self.info.draw()
			self.story.draw()
			
	def on_key_press(self, button, modifiers):
		if self.info:
			if button == pyglet.window.key.SPACE:
				self.world = World(0)
				self.world.add("knight",300.0,64.0)
				self.world.add("geometry",0,0,w=800,h=16)
				self.world.add("player",300.0,700.0)
		
				for i in range(0, 50):
					self.world.add("potato",0,0)
				
				self.world.init()
				self.info = False
				Main.coin.play()
			else:
				return
		if self.world.controllable:
			self.world.handleinput(button)
		
	def on_key_release(self, button, modifiers):
		if self.info:
			return
		if self.world.controllable:
			self.world.handleinput(button, release=True)
		
main = Main()
		
if __name__ == '__main__':
	pyglet.clock.schedule_interval(main.update, 1/120.0)
	
	pyglet.app.run()