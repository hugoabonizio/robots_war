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

print 'Sincronizando...'
if client.synced():
	client.listen(tank, enemy, chat)

# init and show screen
pygame.init()
screen = pygame.display.set_mode(size)


# load object
heart = pygame.transform.scale(pygame.image.load("images/heart-icon.png"), (20, 20))


while True:


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	screen.blit(pygame.image.load("images/bg.jpg"), (0, 0))
	font = pygame.font.Font(None, 50)
	
	# if you win
	if tank.win:
		font_render = font.render("Parabens, voce ganhou!!", 1, (255, 255, 255))
		screen.blit(font_render, ((width/2) - 200, (height/2) - 20))

	# if enemy wins
	elif tank.win == False:
		font_render = font.render("Voce perdeu :/", 1, (255, 255, 255))
		screen.blit(font_render, ((width/2) - 100, (height/2) - 20))

	# if connection is ok
	elif tank.ok:
		# background
		screen.blit(pygame.image.load("images/bg.jpg"), (0, 0))
		
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

		# enemy bullets
		for bullet in enemy_bullets:
			bullet.move(enemy=True)
			screen.blit(bullet.obj, bullet.rect)
			# check collision
			if bullet.rect.colliderect(tank):
				enemy_bullets.remove(bullet)
				if tank.life > 0:
					tank.life -= 1
				else:
					client.send('game:dead=true;')

		# render players
		screen.blit(tank.obj, tank.rect)
		screen.blit(enemy.obj, enemy.rect)

		
		
		# render chat

		# render conversation
		font = pygame.font.Font(None, 20)
		last_message_y = 0
		for message in reversed(chat.conversation):
			font_render = font.render(message, 1, (255, 255, 255))
			screen.blit(font_render, (20, 200 + last_message_y))
			last_message_y -= 15

		# render buffer
		font_render = font.render("> " + chat.buffer, 1, (255, 255, 255))
		screen.blit(font_render, (20, 215))


		# render lifes

		# enemy's
		for i in range(enemy.life):
			screen.blit(heart, (width - 40 - (i * 25), 80))

		# tank's
		for i in range(tank.life):
			screen.blit(heart, (20 + (i * 25), 300))



	# if connection error
	else:
		screen.fill([0, 0, 0])
		font_render = font.render("Problema na conexao...", 1, (255, 255, 255))
		screen.blit(font_render, (90, height/2))

	
	pygame.display.flip()
	pygame.time.wait(10)