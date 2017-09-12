from socket import * 
import random

host = "10.0.0.151" # get the ip address of the raspberry pi zero

print host

port = 4447

s = socket(AF_INET, SOCK_STREAM)

print "Socket Made"

s.bind((host, port))

print "Socket Bound"

s.listen(5)

print "Listening for connection..."

q, addr= s.accept()

#data = raw_input("Enter data to be sent: ")

data = random.randint(1,100)

msg = str(data)

print msg

q.send(msg)

s.close
