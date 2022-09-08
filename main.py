import pygame
from sys import exit
from random import randint, choice
# add level
# increasing speeds
from player import Player
from obstacle import Obstacle
from bullet import Bullet
from settings import *

class Game():
	def __init__(self):
		super().__init__()
		self.test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)
		self.game_active = False
		self.score = 0
		self.obstacle_slide_speed = obstacle_slide_speed

		#Sprite Groups
		self.player = pygame.sprite.GroupSingle()
		self.player.add(Player())

		self.obstacle_group_invaders = pygame.sprite.Group()
		self.obstacle_group_invaders.draw(screen)

		self.group_bullets = pygame.sprite.Group()

		self.obstacle_group_bullets = pygame.sprite.Group()

		# Intro screen
		self.intro =True

	def check_collisions(self):
		obstacles = self.obstacle_group_invaders.sprites()
		for obs in obstacles:
			# When the obstacles strike the walls, change direction
			if(obs.rect.right>=width or obs.rect.left<=0):
				self.obstacle_slide_speed=0-self.obstacle_slide_speed
				return True
			# When the obstacles reach bottom, game over
			if(obs.rect.bottom>=self.player.sprite.rect.top):
				return False
			# When any player bullet hits the obstacle
			if pygame.sprite.spritecollide(obs,self.group_bullets,True):
				self.play_fire_sound()
				obs.hits-=1
				if(obs.hits==0):
					obs.kill()
					if(obs.typee == 'red'):
						self.score+=red_score
					if(obs.typee == 'yellow'):
						self.score+=yellow_score
					if(obs.typee == 'green'):
						self.score+=green_score
				return True
		# When any obstacle bullet hits the player, the player life reduce
		if pygame.sprite.spritecollide(self.player.sprite,self.obstacle_group_bullets,True):
			self.player.sprite.lives-=1
			return self.player.sprite.lives>-1
		return self.player.sprite.lives>-1

	def obstacle_down(self):
		self.obstacle_group_invaders.update(True,obstacle_down_speed)

	def obstacle_bullet(self):
		# Getting a Random obstacle to fire bullet from
		obs = self.obstacle_group_invaders.sprites()[randint(0,len(self.obstacle_group_invaders.sprites())-1)]
		x = obs.rect.left + int(obs.rect.right-obs.rect.left)/2
		y = obs.rect.bottom
		self.obstacle_group_bullets.add(Bullet(0-bullet_speed,x,y))

	def player_shoot(self):
		if len(self.group_bullets.sprites()) != 0:
			return
		x = self.player.sprite.rect.left + int(self.player.sprite.rect.right-self.player.sprite.rect.left)/2
		self.group_bullets.add(Bullet( bullet_speed,x,self.player.sprite.rect.top-bullet_height))

	def create_obstacles(self):
		x_start = width/15
		y_start = 30
		for row_index, row in enumerate(shape):
			for col_index,col in enumerate(row):
				if col == 'r':
					x = x_start + col_index * obstacle_size + offset_x
					y = y_start + row_index * obstacle_size
					block = Obstacle('red',x,y, red_obs_hits)
					self.obstacle_group_invaders.add(block)
				if col == 'y':
					x = x_start + col_index * obstacle_size + offset_x
					y = y_start + row_index * obstacle_size
					block = Obstacle('yellow',x,y, yellow_obs_hits)
					self.obstacle_group_invaders.add(block)
				if col == 'g':
					x = x_start + col_index * obstacle_size + offset_x
					y = y_start + row_index * obstacle_size
					block = Obstacle('green',x,y, green_obs_hits)
					self.obstacle_group_invaders.add(block)

	def display_lives(self):
		lives_surf = self.test_font.render('Extra Lives: {}'.format(self.player.sprite.lives),False,(64,64,64))
		lives_surf_rect = lives_surf.get_rect(center = (680,20))
		screen.blit(lives_surf,lives_surf_rect)
  
	def display_message(self, text, center_pos):
		message = self.test_font.render(text,False,(111,196,169))
		message_rect = message.get_rect(center = center_pos)
		screen.blit(message, message_rect)

	def display_inactive_screen(self):
		screen.fill((94,129,162))

		# Player image
		player_stand = pygame.image.load('./graphics/player.png').convert_alpha()
		player_stand = pygame.transform.rotozoom(player_stand,0,2)
		player_stand_rect = player_stand.get_rect(center = (400,200))
		screen.blit(player_stand,player_stand_rect)

		self.display_message('Space Invaders', (400,30))
		self.display_message('Your score: {}'.format(self.score), (400,80))
		self.display_message('Press space to fire', (400,330))

		if self.intro == False :
			if len(self.obstacle_group_invaders.sprites())==0:
				self.display_message('You won', (400,380))
			elif(self.score != 0):
				self.display_message('You Lost', (400,380))
	
	def display_score(self):
		score_surf = self.test_font.render('Score: {}'.format(self.score),False,(64,64,64))
		score_rect = score_surf.get_rect(topleft = (0,0))
		screen.blit(score_surf,score_rect)
	
	def play_fire_sound(self):
		fire_sound = pygame.mixer.Sound('./audio/jump.mp3')
		fire_sound.set_volume(100)
		fire_sound.play()

	def play_music(self):
		bg_music = pygame.mixer.Sound('./audio/music.wav')
		bg_music.set_volume(0.5)
		bg_music.play(loops = -1)

	def run(self):
		if self.game_active:
			screen.fill('Black')

			self.display_score()
			self.display_lives()

			self.player.draw(screen)
			self.player.update()

			self.obstacle_group_invaders.draw(screen)
			self.obstacle_group_invaders.update(False,self.obstacle_slide_speed)

			self.group_bullets.draw(screen)
			self.group_bullets.update()

			self.obstacle_group_bullets.draw(screen)
			self.obstacle_group_bullets.update()

			self.game_active = self.check_collisions()

			if len(self.obstacle_group_invaders.sprites())==0:
				self.game_active = False

		else:
			self.display_inactive_screen()

	def restart(self):
		self.play_music()
		self.player.sprite.rect.midleft = (width/2, height)
		self.player.sprite.lives = num_of_lives
		self.obstacle_group_invaders.empty()
		self.create_obstacles()
		self.group_bullets.empty()
		self.score=0
		self.intro = False


if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((width,height))
	clock = pygame.time.Clock()
	game = Game()

	# Timer 
	obstacle_down_timer = pygame.USEREVENT + 1
	pygame.time.set_timer(obstacle_down_timer,obstacle_down_time)
	obstacle_bullet_timer = pygame.USEREVENT + 2
	pygame.time.set_timer(obstacle_bullet_timer,obstacle_bullet_time)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if game.game_active:
				if event.type == obstacle_down_timer:
					game.obstacle_down()
				if event.type == obstacle_bullet_timer:
					game.obstacle_bullet()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					game.player_shoot()
			else:
				if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
					game.game_active = True
					game.restart()

		game.run()

		pygame.display.update()
		clock.tick(60)