from socket import *
import time
import subprocess

host = "10.0.0.150" #ip address of the server

print host

port = 2004

s=socket(AF_INET, SOCK_STREAM)
#s.settimeout(60)
#s.timeout()
print "socket made"

while True:
	try:
		s.connect((host, port))
#		s.send("Client 1 Connected")
		print "socket connected!!"
		time.sleep(2)
#		msg = s.recv(1024)
#		print "Message from server: ", msg 
		break
	except:
		print "not connection found will try again in 2 seconds..."
		time.sleep(2)

try:
	while True:
		
		msg = raw_input('Enter message for server: ')
		s.send(msg)
		print "Message sent"
#		msg=s.recv(1024)

#		print "Message from server: " + msg	
		time.sleep(1)

except KeyboardInterrupt:
	print "\nClosing"
	s.close

except Exception:
	print "\nOther Raspberry pi close connection"
	print "Close connection"
	s.close
	

def shutdownRPi():
	print "Shutting down"
	command = "/usr/bin/sudo /sbin/shutdown -h now"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output


