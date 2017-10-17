#!/usr/bin/env python

import socket, sys, signal
import threading import Thread


class client_thread():
	def __init__(self, clientsocket, ip, port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.bufferSize = 1024
		self.conn = clientsocket

	def run(self):
		while 1:
			data = self.conn.recv(self.bufferSize)
			if not data:
				break
			print "receive data: ", data
			self.conn.send(data) # echo


def init(Port):
    host = 'localhost'
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((host, Port))
    serversocket.listen(4)
    signal.signal(signal.SIGPIPE, signal.SIG_IGN) # IGNORE SIG_PIPE
    return serversocket

def run(serversocket, bufferSize, port):
	while 1:
	        (clientsocket, address) = serversocket.accept()
        	ct = client_thread(clientsocket, 'localhost', port)
        	ct.run()

def cleanup(serversocket):
	serversocket.close()
	print "Closing connection"


###################### Main Code ################

if len(sys.argv) != 2:
    print "Usage: <Server Port>"
    raise SystemExit(1)

port = int(sys.argv[1])

bufferSize  = 1024
serversocket = init(port)
run(serversocket, bufferSize, port)
cleanup()
