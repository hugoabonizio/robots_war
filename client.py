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
        print 'testando synced'
        response = self.client.recv(4)
        print 'response: ', response
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
                elif header == 'chat':
                    key, value = body.split('=')
                    chat.add_message(key, value)
    except Exception as msg:
        print "exce: ", msg, header, body
    connection.close()

def sender(connection, tank, enemy):
    try:
        while True:
            connection.send('game:position=' + str(tank.rect.left) + ';')
            pygame.time.wait(20)
    except Exception as msg:
        print "Excecao: ", msg
    connection.close()