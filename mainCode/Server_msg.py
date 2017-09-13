from socket import * 
import random
import time

host = "10.0.0.151" # ip address of the server

print host

port = 4447

s = socket(AF_INET, SOCK_STREAM)

print "Socket Made"

s.bind((host, port))

print "Socket Bound"


s.listen(5)

print "Listening for connection..."

q, addr= s.accept()
print "Connected to address: ", addr
w, addr2=s.accept()
print "Connected to addres: ", addr2

clientN1 = q.recv(1024)
print "who is on? ", clientN1
q.send("Thank you for connecting")

clientN2 = w.recv(1024)
print "who is on? ", clientN2
w.send("Thank you for connection")


try:
	while True:
		msg1 = q.recv(1024)
		print "Sending Original mesage: ", msg1
		msgBack1 = msg1 + " Got your message Client"
		q.send(msgBack1)

		msg2 = w.recv(1024)
		print "Sending Original mesage: ", msg2
                msgBack2 = msg2 + " Got your message Client"
                q.send(msgBack2)		

except KeyboardInterrupt: 
	print "Closing connection"
	s.close

