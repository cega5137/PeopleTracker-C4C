print "Register GPIO" 
import time 
import datetime 
import socket 
from UltraSonicSensor import UltraSonic
from switch import Switch

def readInitialization(file):
        fid = open(file,"r")
        data = fid.read()
        dataSplit = data.split()
        for i in [0,2,4]:
                with Switch(dataSplit[i]) as case:
                        if case('Station:'):
                                Station = dataSplit[i+1]
				#print "Station: ", Station
                        if case('ipaddr:'):
                                ipaddr = dataSplit[i+1]
				#print "ipaddr: ", ipaddr
                        if case('port:'):
                                port = int(dataSplit[i+1])
				#print "port: ", port

        return [Station, ipaddr, port]


TRIG = 23
ECHO = 24

print "Starting Application..."
Counter = UltraSonic(TRIG,ECHO)

# Read initialization file
[Station, ipaddr, port] = readInitialization("initializationFile")
print Station
print ipaddr
print port

#Station
#Station = "Asian"
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
#host = "10.0.0.150"
#port = 3333
BUFFER_SIZE = 2000
Sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while 1:
	try:
		T0 = time.time()
		Sc.connect((ipaddr, port))
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
			if ((T.microsecond/1000) < 700) and T.second == 0:
				n = n + 1
        			previousTimeCount = masterCount - previousTimeCount;
				print "Saving time is: ", T
	        		#### Sending data
				msg = Station + " {} {} ".format(previousTimeCount, masterCount)
				while True:
					try:
						Sc.send(msg)
						break
					except:
						try:
							Sc.connect((ipaddr, port))
							print "Connected again"
						except:
							print "Could not send data"
							time.sleep(0.5)
#				State = Sc.recv(BUFFER_SIZE)
#				print "Raspberry pi State: ", State
				previousTimeCount = masterCount
				T = datetime.datetime.time(datetime.datetime.now())
				time.sleep(0.1)
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


'''
def readInitialization(file):
	fid = open(file,"r")
	data = fid.read()
	dataSplit = data.split()
	for i in [0,2,4]:
		with Switch(dataSplit[i]) as case:
			if case('Station'):
				Station = dataSplit[i+1]
			if case('ipaddr'):
				ipaddr = dataSplit[i+1]
			if case('port'):
				port = int(dataSplit[i+1])

	return [Station, ipaddr, port]

		
'''
