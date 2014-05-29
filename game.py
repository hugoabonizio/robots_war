import sys, pygame
from bullet import Bullet
from tank import Tank
from chat import Chat
from config import *
import client



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


# initialize chat
chat = Chat(client)
chat.add_message('you', 'hahaha1')
chat.add_message('you', 'hahaha2')
chat.add_message('you', 'hahaha3')
chat.add_message('you', 'hahaha4')


print 'Sincronizando...'
if client.synced():
	client.listen(tank, enemy, chat)

# init and show screen
pygame.init()
screen = pygame.display.set_mode(size)


while True:

	# background
	screen.fill([0, 0, 0])
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			# chat functions
			if (event.key > 96 and event.key < 123) or event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == 8:
				if event.key == pygame.K_RETURN:
					chat.send()
				elif event.key == 8:
					chat.backspace()
				else:
					chat.write(event.key)
			else:
				# moving
			 	if event.key == pygame.K_LEFT:
			 		tank.direction = 'left'
			 	if event.key == pygame.K_RIGHT:
			 		tank.direction = 'right'
			 	# shoot
			 	if event.key == pygame.K_UP:
			 	    if len(bullets) < 2:
			 	    	tank.shoot()
			 	    	client.send_bullet(tank.rect.left)

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

	# enemy bullets
	for bullet in enemy_bullets:
		bullet.move(enemy=True)
		screen.blit(bullet.obj, bullet.rect)

	# render players
	screen.blit(tank.obj, tank.rect)
	screen.blit(enemy.obj, enemy.rect)

	
	
	# render chat

	# render conversation
	font = pygame.font.Font(None, 20)
	last_message_y = 0
	for message in reversed(chat.conversation):
		font_render = font.render(message, 1, (255, 255, 255))
		screen.blit(font_render, (20, 300 + last_message_y))
		last_message_y -= 15

	# render buffer
	font_render = font.render("> " + chat.buffer, 1, (255, 255, 255))
	screen.blit(font_render, (20, 315))


	
	pygame.display.flip()
	pygame.time.wait(10)