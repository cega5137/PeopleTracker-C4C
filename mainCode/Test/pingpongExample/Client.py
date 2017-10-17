#!/usr/bin/env python 

import socket
import time

TCP_IP = '10.0.0.150'
TCP_PORT = 3333
bufferSize = 1024
msg = "working"
s = socket.scoket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))


try:
	while True:
		s.send(msg)
		data = s.recv(bufferSize)
		msg = data
		time.sleep(5)

except:
	s.close()
