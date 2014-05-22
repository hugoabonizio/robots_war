from socket import *
import threading
import thread
import sys

slots = 2

def handler(clientsock, addr):
    global slots
    while True:
        data = clientsock.recv(BUFSIZ)
        if not data:
            break
        msg = 'echoed: ' + data
        clientsock.send(msg)
    print 'acabou uma iteracao'
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
            thread.start_new_thread(handler, (clientsock, addr))
            print '...connected from:', addr
        else:
            print 'closing..'
            clientsock.send('close')
            clientsock.close()