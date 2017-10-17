#!/usr/bin/env python

import socket

TCP_IP = '10.0.0.150'
TCP_PORT = 3333
bufferSize = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(4)

conn, addr = s.accept()
print 'Connection address: ', addr

while 1:
	data = conn.recv(bufferSize)
	if not data: 
		conn.close()

	print "Receive: ", data
	conn.send(data)

