import pygame
from bullet import Bullet
from config import bullets

class Tank:
	def __init__(self, left, top, rotate = True):
		self.obj = pygame.image.load("images/tank.gif")
		if rotate: self.obj = pygame.transform.rotate(self.obj, 180)
		self.rect = self.obj.get_rect(center=(left, top))
		self.direction = 'stopped'
		self.life = 4

	def move(self):
		if self.direction == 'left':
			speed = [-2, 0]
		elif self.direction == 'right':
			speed = [2, 0]
		else:
			speed = [0, 0]
		self.rect = self.rect.move(speed)

	def shoot(self):
		bullet = Bullet(self.rect.left + 20, self.rect.top)
		bullets.append(bullet)