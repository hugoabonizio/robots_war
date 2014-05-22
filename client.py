import sys
import socket

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    client.connect(('localhost', int(sys.argv[1])))
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