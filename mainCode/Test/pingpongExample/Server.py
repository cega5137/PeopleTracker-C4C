#!/usr/bin/env python

import socket, sys

def init(Port):
	s = accept(Port)

	return connect(s)

def accept(port):
	host = 'localhost' #'10.0.0.150'
        print "IP: ", host
        print "PORT: ", Port

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, Port))
        s.listen(4)

	return s

def connect(s):
	conn, addr = s.accept()
        print 'Connection address: ', addr
	
	return conn


def run(conn, bufferSize):
	while 1:
		data = conn.recv(bufferSize)
		if not data: 
			cleanup()

		print "Receive: ", data
		conn.send(data)

def cleanup(conn):
	conn.close()
	print "Closing connection"


###################### Main Code ################

if len(sys.argv) != 2:
    print "Usage: <Server Port>"
    raise SystemExit(1)

Port = int(sys.argv[1])

bufferSize  = 1024
conn = init(Port)
run(conn, bufferSize)
cleanup()
