from socket import *
import time

host = " 10.0.0.150"

print host

port = 3333

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

print "socket connected!!"

msg=s.recv(1024)

print "Message from server: " + msg

s.close
