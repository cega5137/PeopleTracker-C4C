#!/usr/bin/env python 

import socket, time, sys

def init_comm(TCP_IP, TCP_PORT):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP,TCP_PORT))

	return s

def run(s,msg):
	try:
		while True:
			print "Sending: ", msg
			s.send(msg)
			data = s.recv(bufferSize)
			print "Message Receive: ", data
			msg = data
			time.sleep(5)

	except:
		s.close()


############################## Main Code ##################
if len(sys.argv) != 3:
    print "Usage: <hostname>, <port>"
    raise SystemExit(1)
host = sys.argv[1]
port = sys.argv[2]

bufferSize = 1024
msg = raw_input("What msg would you like to send? ")

s = init_comm(host, port)
run(s, msg)
