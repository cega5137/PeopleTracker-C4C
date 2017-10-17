#!/usr/bin/env python

import socket, sys

def init_communication(Port):
	TCP_IP = 'localhost' #'10.0.0.150'
	print "IP: ", TCP_IP
	print "PORT: ", Port

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, Port))
	s.listen(4)

	conn, addr = s.accept()
	print 'Connection address: ', addr

	return conn

def run(conn, bufferSize):
	while 1:
		data = conn.recv(bufferSize)
		if not data: 
			conn.close()

		print "Receive: ", data
		conn.send(data)

###################### Main Code ################

if len(sys.argv) != 2:
    print "Usage: <Server Port>"
    raise SystemExit(1)

Port = sys.argv[1]

bufferSize  = 1024
conn = init_communication(Port)
run(conn, bufferSize)
