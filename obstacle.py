import pygame 
from settings import *
class Obstacle(pygame.sprite.Sprite):
'''This class contains the attributes of an obstacle'''
	def __init__(self,typee,x,y,hits):
		super().__init__()
		self.image = pygame.image.load('./graphics/{}.png'.format(typee)).convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))
		self.hits = hits
		self.typee = typee

	def update(self, down,speed):
		if(down):
			self.rect.bottom += speed
		else:
			self.rect.left += speed