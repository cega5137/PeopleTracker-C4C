from socket import *
import time

host = " 10.0.0.150" #ip address of the server

print host

port = 4447

s=socket(AF_INET, SOCK_STREAM)
#s.settimeout(60)
#s.timeout()
print "socket made"

while True:
	try:
		s.connect((host, port))
		break
	except:
		print "not connection found will try again in 2 seconds..."
		time.sleep(1)

try:
	while True:

		print "socket connected!!"

		msg=s.recv(1024)

		print "Message from server: " + msg

		s.send(msg)
		
except KeyboardInterrupt:
	print "\nClosing"
	s.close