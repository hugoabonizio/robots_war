import pygame
from config import size, width, height, bullets, enemy_bullets

class Bullet:
	def __init__(self, left, top):
		self.obj = pygame.image.load("images/bullet.png")
		self.obj = pygame.transform.rotate(self.obj, 180)
		self.rect = self.obj.get_rect(center=(left, top))

	def move(self, enemy=False):
		if enemy:
			speed = 2
		else:
			speed = -2
		self.rect = self.rect.move([0, speed])
		if self.rect.top < 0 or self.rect.top > height:
			if enemy:
				enemy_bullets.remove(self)
			else:
				bullets.remove(self)