import sys
import socket
import thread
import pygame.time

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


    def send(self):
        try:
            if client.recv(1024) == 'close':
            	print 'haaa'
            	raise Exception
            send = 'aa'
            while send != 'sai':
            	send = raw_input()
            	client.send(send)
            	print client.recv(1024)
            client.shutdown(socket.SHUT_RDWR)
            client.close()
        except Exception as msg:
            print msg

    def listen(self, tank, enemy):
        self.tank = tank
        self.enemy = enemy
        thread.start_new_thread(receiver, (self.client, self.tank, self.enemy))
        thread.start_new_thread(sender, (self.client, self.tank, self.enemy))

    def send_bullet(self, left):
        self.client.send('game:bullet=' + left + ';')


def receiver(connection, tank, enemy):
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            print data
            data = data.split(';')[0]
            header, body = data.split(':')
            if header == 'game':
                key, value = body.split('=')
                if key == 'position':
                    enemy.rect.left = int(value)
    except Exception as msg:
        print msg, header, body
    connection.close()

def sender(connection, tank, enemy):
    try:
        while True:
            connection.send('game:position=' + str(tank.rect.left) + ';')
            pygame.time.wait(20)
    except Exception as msg:
        print msg
    connection.close()