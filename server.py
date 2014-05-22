from socket import *
import threading
import thread
import sys
import pygame

slots = 2
connections = [0, 0]

def handler(clientsock, slot):
    global slots, connections
    try:
        clientsock.send('conn')

        connections[int(slot)] = clientsock

        # while there is not other connection in
        # slot, wait the connection
        while connections[int(not slot)] == 0:
            clientsock.send('wait')
            pygame.time.wait(100)
        clientsock.send('sync')
        
        while True:
            data = clientsock.recv(BUFSIZ)
            if not data:
                break
            connections[int(not slot)].send(data)
        print 'acabou uma iteracao'
    except Exception as msg:
        print msg
    clientsock.close()
    slots += 1

if __name__ == '__main__':
    HOST = 'localhost'
    PORT = int(sys.argv[1])
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.bind(ADDR)
    serversock.listen(2)

    while True:
        print 'waiting for connection...'
        clientsock, addr = serversock.accept()
        if slots > 0:
            print 'slots', slots
            slots -= 1
            thread.start_new_thread(handler, (clientsock, slots))
            print '...', slots, 'connected from:', addr
        else:
            print 'closing..'
            clientsock.send('clos')
            clientsock.close()