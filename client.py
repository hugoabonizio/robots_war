import sys
import socket
import thread
import pygame.time
from config import *

class Client:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def connected(self):
        response = self.client.recv(4)
        if response == 'conn':
            return True
        elif response == 'clos':
            return False

    def synced(self):
        response = self.client.recv(4)
        # print 'response: ', response
        if response == 'wait':
            while response != 'sync':
                response = self.client.recv(4)
        return True


    def send(self, message):
        try:
            self.client.send(message)
        except Exception as msg:
            print msg

    def listen(self, tank, enemy, chat):
        self.tank = tank
        self.enemy = enemy
        thread.start_new_thread(receiver, (self.client, self.tank, self.enemy, chat))
        thread.start_new_thread(sender, (self.client, self.tank, self.enemy))

    def send_bullet(self, left):
        self.client.send('game:bullet=' + str(left) + ';')


def receiver(connection, tank, enemy, chat):
    try:
        while True:
            if tank.win == None and tank.ok:
                data = connection.recv(1024)
                if not data:
                    break
                #print data
                data = data.split(';')
                if data[-1] == '': data = data[:-1]
                
                for d in data:
                    header, body = d.split(':')
                    # GAME message
                    if header == 'game':
                        key, value = body.split('=')
                        if key == 'position':
                            enemy.rect.left = int(value)
                        if key == 'bullet':
                            enemy.shoot(enemy=True)
                        if key == 'life':
                            enemy.life = int(value)
                        if key == 'end':
                            if value == 'connection':
                                tank.ok = False
                                # print 'problema na conexao'
                            elif value == 'you_win':
                                tank.win = True
                                # print 'voce ganhou!!'
                            sys.exit()
                    elif header == 'chat':
                        key, value = body.split('=')
                        chat.add_message(key, value)
            else:
                sys.exit()
    except Exception as msg:
        tank.ok = False
        print "Except (receiver): ", msg, header, body
    connection.close()

def sender(connection, tank, enemy):
    try:
        count = 0
        while True:
            if tank.win == None and tank.ok:
                connection.send('game:position=' + str(tank.rect.left) + ';')
                if count % 5 == 0:
                    connection.send('game:life=' + str(tank.life) + ';')
                    if tank.life == 0:
                        tank.win = False
                        connection.send('game:end=you_win;')
                count += 1
                pygame.time.wait(20)
            else:
                sys.exit()
    except Exception as msg:
        tank.ok = False
        print "Except (sender): ", msg
    connection.close()