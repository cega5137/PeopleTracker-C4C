#!/usr/bin/env python 

import socket, time, sys

def init(host, port):
	return connectToServer(host, port)

def connectToServer(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        while True:
                try:
                        s.connect((host,port))
                        break
                except:
                        print "Server not found. Will try in two second"
                        time.sleep(2)
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
		cleanup(s)

def cleanup(s):
	s.close()
	print "Closing Program"

############################## Main Code ##################
if len(sys.argv) != 3:
    print "Usage: <hostname>, <port>"
    raise SystemExit(1)
host = sys.argv[1]
port = int(sys.argv[2])

bufferSize = 1024
msg = raw_input("What msg would you like to send? ")

s = init(host, port)
run(s, msg)
cleanup(s)
