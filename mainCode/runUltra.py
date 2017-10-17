print "Register GPIO" 
import time 
import datetime 
import socket 
import subprocess 
import signal
from UltraSonicSensor import UltraSonic 
from switch import Switch

from socket import * 


################################### Functions #####################
def readInitialization(file):
	''' 
	readInitialization: 
	'''
        fid = open(file,"r")
        data = fid.read()
        dataSplit = data.split()
        for i in [0,2,4]:
                with Switch(dataSplit[i]) as case:
                        if case('Station:'):
                                Station = dataSplit[i+1]
				with Switch(Station) as station:
					if station('Asian'):
						delayTime = 0
					if station('American'):
						delayTime = 1
					if station('Persian'):
						delayTime = 2
					if station('Italian'):
						delayTime = 3
					if station('Latin'):
						delayTime = 4 
				#print "Station: ", Station
                        if case('ipaddr:'):
                                ipaddr = dataSplit[i+1]
				#print "ipaddr: ", ipaddr
                        if case('port:'):
                                port = int(dataSplit[i+1])
				#print "port: ", port

        return [Station, ipaddr, port, delayTime]

def init_client(initializationFile):
    #Get the initialization file
	[Station, host, port, delayTime, TRIG, ECHO, tol_dist] = readInitialization(initializationFile)
	Counter = UltraSonic(TRIG,ECHO)
	print Station
	print ipaddr
	print port
	
    # Initializes the client
	#signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    
    return [connectToServer(host, port), Counter]

def connectToServer(host, port):
    # Connects to Server
    s=socket(AF_INET, SOCK_STREAM)
    while True:
        try:
            s.connect((host, port))
            print "socket connected!!"
            break
        except:
            print "not connection found will try again in 2 seconds..."
            time.sleep(2)
    return s

def variableDeclaration():
	# Counters
	masterCount = 0
	previousTimeCount = 0

	# bool
	isPerson = 0

	# Timer
	T = datetime.datetime.time(datetime.datetime.now())  
	t_actual = time.time()
	n = 1
	update_time = 1 # minutes
	print "The on time is ", T
	return [masterCount, previousTimeCount, isPerson, t_actual]

def runClient(soc, Counter):
	#set up variable declaration
	[masterCount, previousTimeCount, isPerson, t_actual] = variableDeclaration()

    #Main Loop
    while True:
        # Take Measurment
		T = datetime.datetime.time(datetime.datetime.now())
    		if T.minute == 0 or T.minute == 15 or T.minute == 30 or T.minute == 45:
				if T.second == delayTime:
					previousTotal = sendData(soc, station, countMaster, previousTotal)
        
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
	
 	data = raw_input('Enter message to Server:')#'Station Current Total'#getdata()
	
def sendData(soc, Station, countMaster, previousTotal):
	# Creating message
	previousTimeCount = masterCount - previousTotal
	msg = Station + " {} {} ".format(previousTotal, masterCount
	
	# Send Data
	while True:
		try:
        	bits_written = soc.send(data)#write(data)
			break
		except:
			soc.close()
			soc = connectToServer(host, port)
			
	previousTimeCount = masterCount
	T = datetime.datetime.time(datetime.datetime.now())
	return [masterCount, T]
	
def getData(masterCount):
	print "Begining of Main Loop", T
	print "Master Count = ", masterCount
	print "Current Count = ", (masterCount - previousTimeCount)
	distance = Counter.getDistance()
	    
	if distance > 400:
		#continue
		return masterCount

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
			#continue
			return masterCount
    	
	if isPerson == 1:
    		#Person Was standing in front of sensor
        	if (distance > tol_dist):
        	# Person is no longer standing in front of sensor
            		if (time.time() - time_Person) < 1:
                		isPerson = 0
                		#continue
						return masterCount
						
		    		print "Time In Front = ", time.time() - time_Person
            		masterCount = masterCount + 1
            		isPerson = 0
        else:
        # Person is still standing in front of sensor
            continue
			return masterCount
	#END OF LOOP

def cleanup(soc):
    # Close Socket
    if (soc > 0):
        soc.close()
    # Shutdown pi
    shutdownRPi()

def shutdownRPi():
    print "Shutting down"
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


###########################################################################################
'''
TRIG = 23
ECHO = 24

print "Starting Application..."
Counter = UltraSonic(TRIG,ECHO)

# Read initialization file
[Station, ipaddr, port, delayTime] = readInitialization("initializationFile")
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
				if T.second == delayTime:
					#n = n + 1
	        		previousTimeCount = masterCount - previousTimeCount
					print "Saving time is: ", T
		        	#### Sending data
					msg = Station + " {} {} ".format(previousTimeCount, masterCount)
					while True:
						try:
							Sc.send(msg)
							break
						except:
							try:
								Sc.close()
								Sc.connect((ipaddr, port))
								print "Connected again"
							except:
								print "Could not send data"
								time.sleep(0.5)
	#				State = Sc.recv(BUFFER_SIZE)
	#				print "Raspberry pi State: ", State
					previousTimeCount = masterCount
					T = datetime.datetime.time(datetime.datetime.now())
					time.sleep(1)
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
	
##################################### New Main ####################


# Read initialization file
filePath = "initializationFile"
#[Station, host, port, delayTime] = readInitialization("initializationFile")
#Counter = UltraSonic(TRIG,ECHO)
#print Station
#print ipaddr
#print port
#host = "10.0.0.150" #ip address of the server
#port = 2004
#print "hostname: ", host, " Portnumber: ", port

# Initalize Client
[soc, Counter] = init_client(filePath)
runClient(soc)
cleanup(soc)



