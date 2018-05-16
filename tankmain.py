#encoding:utf-8
from __future__ import division
import sys, pygame, time, random
from pygame.locals import *
'''this is a tank game
gino change for test
'''
class TankMain(object):
	width  = 600
	print sys.path
	height = 500
	mytank = None
	my_cannon_list = []
	explode_list = []
	#enemy_list = []
	enemy_list = pygame.sprite.Group()
	enemy_cannon_list = pygame.sprite.Group()
	walls = []
	def __init__(self):
		pass

	def start_game(self):
		pygame.init()
		screen = pygame.display.set_mode((TankMain.width, TankMain.height), 0, 32)
		pygame.display.set_caption('Tank Game')
		TankMain.mytank = Player_Tank(screen)
		for i in range(1, 6):
			TankMain.enemy_list.add(Enemy_Tank(screen))
		TankMain.walls.append(Wall(screen,150,330,100,20))
		TankMain.walls.append(Wall(screen,350,330,100,20))

		while True:
			screen.fill((0, 0, 0))
			screen.blit(self.show_info(), (0, 5))
			self.get_event(TankMain.mytank, screen)
			for wall in  TankMain.walls:
				wall.display()
				wall.hit_other()

			if TankMain.mytank and TankMain.mytank.live:
				TankMain.mytank.display()
				TankMain.mytank.move()
				for cannon in TankMain.my_cannon_list:
					if cannon.live:
						cannon.display()
						cannon.hit()
						cannon.move()
					else:
						TankMain.my_cannon_list.remove(cannon)
			if  not  TankMain.mytank.live:
				TankMain.mytank  == None
			for tank in TankMain.enemy_list:
				tank.display()
				tank.random_fire()
				tank.get_random_move()
			for cannon in TankMain.enemy_cannon_list:
				if cannon.live and TankMain.mytank.live:
					cannon.hit(TankMain.mytank)
					cannon.move()
					cannon.display()
				else:
					TankMain.enemy_cannon_list.remove(cannon)
			for explode in TankMain.explode_list:
				explode.display()

			if len(TankMain.enemy_list) < 5:
				TankMain.enemy_list.add(Enemy_Tank(screen))
			pygame.display.update()
			time.sleep(0.05)



	def stop_game(self):
		sys.exit()
	#
	def show_info(self):
		font = pygame.font.SysFont('microsoftyahei', 15)
		text_sf = font.render("remain:%d"%len(TankMain.enemy_list), True, (255, 0, 0))
		return text_sf

	def get_event(self, mytank, screen):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.stop_game()
			#print event.type
			#print mytank
			if event.type == KEYDOWN and not mytank.live and event.key == K_n:
				TankMain.mytank = Player_Tank(screen)
				TankMain.mytank.live = True
			if event.type == KEYDOWN and mytank:
				if event.key == K_LEFT:
					mytank.direction ='Left'
					mytank.stop = False
					#mytank.move()
				if event.key == K_RIGHT:
					mytank.direction ='Right'
					mytank.stop = False
					#mytank.move()
				if event.key == K_UP:
					mytank.direction ='Up'
					mytank.stop = False
					#mytank.move()
				if event.key == K_DOWN:
					mytank.direction ='Down'
					mytank.stop = False
					#mytank.move()
				if event.key == K_SPACE:
					ca = mytank.fire()
					ca.good = True
					TankMain.my_cannon_list.append(ca)
			if event.type == KEYUP and mytank:
				if event.key == K_LEFT or K_DOWN or K_RIGHT or K_UP:
					mytank.stop = True

class BaseItem(pygame.sprite.Sprite):


	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class Tank(BaseItem):
	width  = 30
	height = 30
	def __init__(self, screen, left, top):
		super(BaseItem, self).__init__()
		self.screen = screen
		self.direction='Down' #默认方向
		self.speed =3
		self.images={} #所有方向图片
		self.images['Down'] = pygame.image.load('images/tankDown.png') #定义导入坦克默认方向图片
		self.images['Up'] = pygame.image.load('images/tankUp.png')
		self.images['Right'] = pygame.image.load('images/tankLeft.png')
		self.images['Left'] = pygame.image.load('images/tankRight.png')
		self.image = self.images[self.direction]
		self.live = True
		self.rect = self.image.get_rect()
		self.rect.left = left
		self.rect.top  = top
		self.stop = False
		self.lastleft = self.rect.left
		self.lasttop  = self.rect.top

	def display(self):
		self.image = self.images[self.direction]
		self.screen.blit(self.image, self.rect)

	def move(self):
		#print self.direction
		if not self.stop:
			self.lastleft = self.rect.left
			self.lasttop  = self.rect.top
			if self.direction == "Left":
				if self.rect.left > self.speed:
					self.rect.left -= self.speed
				else:
					self.rect.left = self.speed
			elif self.direction =='Right':
				if self.rect.right < TankMain.width - self.speed:
					self.rect.right += self.speed
				else:
					self.rect.right= TankMain.width - self.speed
			elif self.direction =='Up':
				if self.rect.top > self.speed:
					self.rect.top -= self.speed
				else:
					self.rect.top = self.speed
			elif self.direction =='Down':
				if self.rect.bottom < TankMain.height:
					self.rect.bottom += self.speed
				else:
					self.rect.bottom = TankMain.height

	def fire(self):
		cannon = Cannon(self.screen,self)
		return cannon

	def stay(self):
		self.rect.left = self.lastleft
		self.rect.top  = self.lasttop

class Player_Tank(Tank):
	def __init__(self, screen):
		Tank.__init__(self, screen,300 ,400)
		self.stop = True
		self.direction = 'Up'
		#super(Tank, self).__init__()
		self.speed = 6

	def fire(self):
		cannon = Player_Cannon(self.screen,self)
		return cannon
class Enemy_Tank(Tank):

	def __init__(self,screen):
		Tank.__init__(self, screen, random.randint(0, 500), random.randint(1,30))
		self.step = 10
		self.get_random_direction()

	def get_random_direction(self):
		status = random.randint(0,5)
		if status == 0:
			self.stop = True
		elif status == 1:
			self.direction = 'Right'
			self.stop = False
		elif status == 2:
			self.direction = 'Left'
			self.stop = False
		elif status == 3:
			self.direction = 'Up'
			self.stop = False
		elif status == 4:
			self.direction = 'Down'
			self.stop = False

	def get_random_move(self):
		if self.live:
			if self.step == 0:
				self.get_random_direction()
				self.step =10
			else:
				self.move()
				self.step -= 1
	def random_fire(self):
		r = random.randint(0,50)
		if r > 45:
			m = self.fire()
			TankMain.enemy_cannon_list.add(m)
		else:
			return

class Cannon(BaseItem):
	width = 12
	height = 12
	def __init__(self, screen, tank):
		BaseItem.__init__(self)
		#super().__init__(self)
		self.speed = 12
		self.good = False
		self.tank = tank
		self.tank_rect = tank.rect
		self.screen = screen
		self.direction = tank.direction
		self.image= pygame.image.load('l:\\tankgame\\images\\cannonenemy.png')
		self.live = True
		self.rect = self.image.get_rect()
		if self.direction == 'Down' or self.direction == 'Up':
			self.rect.left = (tank.rect.right - tank.rect.left)/ 2 + tank.rect.left - self.width /2
			self.rect.top =  tank.rect.top
		else:
			self.rect.left = tank.rect.left
			self.rect.top = (tank.rect.bottom - tank.rect.top) /2 + tank.rect.top - self.height /2

	def move(self):
		if self.live:
			if self.direction == "Left":
				if self.rect.left > self.speed:
					self.rect.left -= self.speed
				else:
					self.live = False
			elif self.direction =='Right':
				if self.rect.right < TankMain.width - self.speed:
					self.rect.right += self.speed
				else:
					self.live = False
			elif self.direction =='Up':
				if self.rect.top > self.speed:
					self.rect.top -= self.speed
				else:
					self.live = False
			elif self.direction =='Down':
				if self.rect.bottom < TankMain.height:
					self.rect.bottom += self.speed
				else:
					self.live = False

	def display(self):
		self.screen.blit(self.image, self.rect)


	def hit(self,mytank):
		hit_list = pygame.sprite.spritecollide(mytank,TankMain.enemy_cannon_list, False)
		for hit in hit_list:
			TankMain.mytank.live = False
			hit.live = False
			TankMain.enemy_cannon_list.remove(hit)
			explode = Explode(self.screen, hit.rect)
			explode.live = True
			TankMain.explode_list.append(explode)



class Enemy_Cannon(Cannon):
	def __init__(self):
		super(Cannon, self).__init__()


	def hit(self,mytank):
		hit_list = pygame.sprite.spritecollide(mytank,TankMain.enemy_cannon_list, False)
		for hit in hit_list:
			mytank.live = False
			hit.live = False
			TankMain.enemy_cannon_list.remove(hit)
			explode = Explode(self.screen, hit.rect)
			explode.live = True
			TankMain.explode_list.append(explode)

class Player_Cannon(Cannon):
	def __init__(self,screen,tank):
		Cannon.__init__(self,screen,tank)
		#super(Cannon, self).__init__()
		self.image= pygame.image.load('l:\\tankgame\\images\\cannon_player.png')
		#self.rect = tank.rect

	def hit(self):
		if self.good:
			hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_list, False)
			for hit in hit_list:
				hit.live = False
				self.live = False
				TankMain.enemy_list.remove(hit)
				explode = Explode(self.screen, hit.rect)
				explode.live = True
				TankMain.explode_list.append(explode)
				#

class Explode(BaseItem):
	def __init__(self, screen, rect):
		BaseItem.__init__(self)
		self.live = False
		self.screen = screen
		self.images = [pygame.image.load('l:\\tankgame\\images\\explode1_org_new.png'),\
					   pygame.image.load('l:\\tankgame\\images\\explode2_org_new.png'), \
					   pygame.image.load('l:\\tankgame\\images\\explode3_org_new.png'), \
					   pygame.image.load('l:\\tankgame\\images\\explode4_org_new.png'), \
					   pygame.image.load('l:\\tankgame\\images\\explode5_org_new.png'), \
					   pygame.image.load('l:\\tankgame\\images\\explode6_org_new.png'), \
					   pygame.image.load('l:\\tankgame\\images\\explode7_org_new.png'),\
					   pygame.image.load('l:\\tankgame\\images\\explode8_org_new.png'),\
					   pygame.image.load('l:\\tankgame\\images\\explode9_org_new.png')]
		self.image = None

		self.step = 0
		'''
		print rect
		print('rect.left: %s'%rect.left)
		print('rect.right:%s'%rect.right)
		print('rect.top:%s'%rect.top)
		print('rect.bottom:%s'%rect.bottom)
		print('Cannon.width:%s'%Cannon.width)
		left   = rect.left   + (rect.right - rect.left - Cannon.width) / 2
		right  = rect.left   + (rect.right - rect.left + Cannon.width) / 2
		top    = rect.top    + (rect.bottom - rect.top - Cannon.height) / 2
		bottom = rect.top    + (rect.bottom - rect.top + Cannon.height) / 2
		print('.left: %s'%left)
		print('.right:%s'%right)
		print('.top:%s'%top)
		print('.bottom:%s'%bottom)
		rect.left = left
		rect.right = right
		rect.top=top
		rect.bottom =bottom
		print rect
		self.rect = rect
		print self.rect

		'''
		self.rect = rect


	def display(self):
		if self.live:
			if self.step == len(self.images):
				self.live = False
			else:
				self.image = self.images[self.step]
				self.screen.blit(self.image, self.rect)
				self.step += 1
		else:
			return

class Wall(BaseItem):
	def __init__(self, screen, left, top, right, bottom):
		#BaseItem.__init__()
		super(BaseItem, self).__init__()
		self.rect = pygame.Rect(left, top, right, bottom)
		self.color = (255,0,0)
		self.screen = screen
		'''
		self.screen = screen
		self.left = left
		self.top  = top
		self.right = right
		self.bottom = bottom
		'''

	def display(self):
		self.screen.fill(self.color, self.rect)

	def hit_other(self):
		if TankMain.mytank:
			is_hit = pygame.sprite.collide_rect(self, TankMain.mytank)
			if is_hit:
				TankMain.mytank.stop = True
				TankMain.mytank.stay()
		if len(TankMain.enemy_list) > 0 :
			hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_list, False)
			for hit in hit_list:
				hit.stay()

		if len(TankMain.enemy_cannon_list) > 0 :
			hit_list = pygame.sprite.spritecollide(self,TankMain.enemy_cannon_list, False)
			for hit in hit_list :
				TankMain.enemy_cannon_list.remove(hit)
		if len(TankMain.my_cannon_list) > 0 :
			hit_list = pygame.sprite.spritecollide(self,TankMain.my_cannon_list, False)
			for hit in hit_list :
				TankMain.my_cannon_list.remove(hit)






game = TankMain()
game.start_game()