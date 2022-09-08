import pygame
from settings import *
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load('./graphics/player.png').convert_alpha()
		self.rect = self.image.get_rect(midleft = (int(width/2),height))
		self.lives=num_of_lives

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and self.rect.left>=slide_dist:
			self.rect.left-=slide_dist
		if keys[pygame.K_RIGHT] and self.rect.right<=width-slide_dist:
			self.rect.left+=slide_dist

	def update(self):
		self.player_input()