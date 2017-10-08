from socket import *
import time
import subprocess
import datetime

host = " 10.0.0.150" #ip address of the server

print host

port = 3333

s=socket(AF_INET, SOCK_STREAM)
#s.settimeout(60)
#s.timeout()
Station = "Italian"
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

		T = datetime.datetime.time(datetime.datetime.now())

		if T.minute == 0 or T.minute == 15 or T.minute == 30 or T.minute == 45:
			if ((T.microsecond/1000) < 300) and T.second == 0:
                                print "sending data"
				n = n + 1
				masterCount = 1
				previousTimeCount = 2
                                print "Saving time is: ", T
                                #### Sending data
                                msg = Station + " {} {} ".format(previousTimeCount, masterCount)
                                s.send(msg)
                                State = s.recv(BUFFER_SIZE)
                                print "Raspberry pi State: ", State
                                T = datetime.datetime.time(datetime.datetime.now())
                                print "End of the if statement"

#		
#		msg = "This is client1"
#		s.send(msg)
#		print "Message sent"
#		msg=s.recv(1024)

#		print "Message from server: " + msg	
#		time.sleep(1)

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

if __name__ == "__main__":
	print "Hello"
