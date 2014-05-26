import sys, pygame
from bullet import Bullet
from tank import Tank
from config import size, width, height, bullets
import client

pygame.init()

screen = pygame.display.set_mode(size)


tank = Tank(width/2, height - 20)
enemy = Tank(width/2, 20, rotate = False)

# estabilish connect, have to receive
# 'conn' to be in the game
client = client.Client(sys.argv[1], int(sys.argv[2]))
print 'Conectando ao servidor...'
if client.connected():
	print 'OK!'
else:
	print 'Nao ha espaco livre no servidor'
	sys.exit()

print 'Sincronizando...'
if client.synced():
	client.listen(tank, enemy)

while True:

	# background
	screen.fill([0, 0, 0])
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			# moving
		 	if event.key == pygame.K_LEFT:
		 		tank.direction = 'left'
		 	if event.key == pygame.K_RIGHT:
		 		tank.direction = 'right'
		 	# shoot
		 	if event.key == pygame.K_SPACE:
		 	    if len(bullets) < 2: tank.shoot()
		elif event.type == pygame.KEYUP:
			tank.direction = 'stopped'

	# make the tank movement
	tank.move()

	# bullets
	for bullet in bullets:
		bullet.move()
		screen.blit(bullet.obj, bullet.rect)
		if bullet.rect.colliderect(enemy):
			bullets.remove(bullet)
			if enemy.life > 1:
				enemy.life -= 1
			else:
				print 'perdeu, otario!'
			print 'lol'

	# render players
	screen.blit(tank.obj, tank.rect)
	screen.blit(enemy.obj, enemy.rect)
	
	pygame.display.flip()
	pygame.time.wait(10)