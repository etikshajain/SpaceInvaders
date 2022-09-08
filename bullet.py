import pygame
from settings import *
class Bullet(pygame.sprite.Sprite):
	def __init__(self,speed,x,y):
		super().__init__()
		self.speed=speed
		self.image = pygame.Surface((bullet_width,bullet_height))
		self.image.fill('White')
		self.rect = pygame.Rect(x,y,bullet_width,bullet_height)

	def destroy(self):
		if self.rect.top <= 0 or self.rect.bottom>height+100:
			self.kill()
	def update(self):
		self.rect.top-=self.speed
		self.destroy()