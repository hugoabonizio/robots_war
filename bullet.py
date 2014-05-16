import pygame
from config import size, width, height, bullets

class Bullet:
	def __init__(self, left, top):
		self.obj = pygame.image.load("images/bullet.png")
		self.obj = pygame.transform.rotate(self.obj, 180)
		self.rect = self.obj.get_rect(center=(left, top))

	def move(self):
		self.rect = self.rect.move([0, -2])
		if self.rect.top < 0 or self.rect.top > height:
			bullets.remove(self)