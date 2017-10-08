print "Register GPIO" 
import time 
import datetime 
import socket 
from UltraSonicSensor import UltraSonic

TRIG = 23
ECHO = 24

print "Starting Application..."
Counter = UltraSonic(TRIG,ECHO)

#Station
Station = "American"

#Determines if person is standing in range or not
tol_dist = 80

# Counters
masterCount = 0
previousTimeCount = 0
Counter_Person = 0

# bool
isPerson = 0

# Timer
T = datetime.datetime.time(datetime.datetime.now()) 
t_start = time.time()
t_actual = t_start
n = 1
update_time = 1 # minutes
print "The on time is ", T

# Set up host
host = "10.0.0.150"
port = 3333
BUFFER_SIZE = 2000
Sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while 1:
	try:
		T0 = time.time()
		Sc.connect((host, port))
		Tend = time.time()
		print "Time that it takes to connect: ", (Tend - T0)
		print "Connected with server"
		break
	except KeyboardInterrupt:
		Sc.close()
	except:
                print "Could not connect will try in 2 seconds"
                time.sleep(2)

#Start of Loop
try:
	while 1:
    		T = datetime.datetime.time(datetime.datetime.now())
    		if T.minute == 0 or T.minute == 15 or T.minute == 30 or T.minute == 45:
			if ((T.microsecond/1000) < 300) and T.second == 0:
				n = n + 1
        			previousTimeCount = masterCount - previousTimeCount;
				print "Saving time is: ", T
	        		#### Sending data
				msg = Station + " {} {} ".format(previousTimeCount, masterCount)
				Sc.send(msg)
#				State = Sc.recv(BUFFER_SIZE)
#				print "Raspberry pi State: ", State
				previousTimeCount = masterCount
				T = datetime.datetime.time(datetime.datetime.now())
				print "End of the if statement"

    		print "Begining of Main Loop", T
    		print "Master Count = ", masterCount
		print "Current Count = ", (masterCount - previousTimeCount)
	    	distance = Counter.getDistance()
		    
		if distance > 400:
			continue

		#Commenting line
		print "Distance:",distance,"cm"
		# print "isPerson:", isPerson, "tol_dist =", tol_dist
		# No person previously standing in front of sensor
		if isPerson == 0:
			if distance <= tol_dist :
			# Person is now standing in front of sensor
				isPerson = 1
				time_Person = time.time()
			else:
			# No person is standing in front of sensor
				continue
	    	
		if isPerson == 1:
	    		#Person Was standing in front of sensor
	        	if (distance > tol_dist):
	        	# Person is no longer standing in front of sensor
	            		if (time.time() - time_Person) < 1:
	                		isPerson = 0
	                		continue
		    		print "Time In Front = ", time.time() - time_Person
	            		masterCount = masterCount + 1
	            		isPerson = 0
	        else:
	        # Person is still standing in front of sensor
	            continue
	#END OF LOOP

# Clean up
except KeyboardInterrupt: 
	print "Ending Application"	
	Sc.close()
	Counter.close()
