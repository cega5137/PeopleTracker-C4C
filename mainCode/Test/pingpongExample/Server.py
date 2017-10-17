#!/usr/bin/env python

import socket, sys

def init(Port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, Port))
    serversocket.listen(4)
    return serversocket

def run(serversocket, bufferSize):
	while 1:
        (clientsocket, address) = serversocket.accept()
		data = clientsocket.recv(bufferSize)
        ct = client_thread(clientsocket)
        ct.run()

def cleanup(conn):
	conn.close()
	print "Closing connection"


###################### Main Code ################

if len(sys.argv) != 2:
    print "Usage: <Server Port>"
    raise SystemExit(1)

port = int(sys.argv[1])

bufferSize  = 1024
serversocket = init(port)
run(serversocket, bufferSize)
cleanup()
