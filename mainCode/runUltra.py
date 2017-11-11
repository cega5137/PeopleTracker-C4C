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
        for i in [0,2,4,6,8,10, 12]:
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
			if case('TRIG:'):
				TRIG = int(dataSplit[i+1])
			if case('ECHO:'):
				ECHO = int(dataSplit[i+1])
			if case('tolerance:'): 
				tol_dist = int(dataSplit[i+1])
			if case('delayTime:'):
				waitPerson = float(dataSplit[i+1])

        return [Station, ipaddr, port, delayTime, TRIG, ECHO, tol_dist, waitPerson]

def init_client(initializationFile):
    #Get the initialization file
	[Station, host, port, sendingDelay, TRIG, ECHO, tol_dist, personDelay] = readInitialization(initializationFile)
	Counter = UltraSonic(TRIG,ECHO)
	print Station
	print host
	print port
	
    # Initializes the client
	#signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    
    	return [connectToServer(host, port), Counter, tol_dist, sendingDelay, Station, host, port, personDelay]

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

def runClient(soc, Counter, tol_dist, sendingDelay, station, host, port, personDelay):
	#set up variable declaration
	[masterCount, previousTotal, isPerson, t_actual] = variableDeclaration()
	
	#Schedule shutdown
	schShut = scheduleShutdown("/home/pi/Documents/Python/PeopleTracker-C4C/mainCode/shutdownTime") #datetime.time(11,35,0,0)

	#Main Loop
	while True:
        # Take Measurment
		T = datetime.datetime.time(datetime.datetime.now())
		if T >= schShut:
			# get on standby funtion
			# get new schShut
			pass

    		if T.minute == 0 or T.minute == 15 or T.minute == 30 or T.minute == 45:
			if T.second == sendingDelay:
				[previousTotal, T] = sendData(soc, host, port, station, masterCount, previousTotal)

		print "Begining of Main Loop", T,
		print "\nMaster Count = ", masterCount,
		print "\nCurrent Count = ", (masterCount - previousTotal),
    		distance = Counter.getDistance()
		#Commenting line
		print "\nDistance:",distance,"cm"

		if distance > 400:
			continue

		
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
	            		if (time.time() - time_Person) < personDelay:
	                		isPerson = 0
	                		continue
		    		print "Time In Front = ", time.time() - time_Person
	            		masterCount = masterCount + 1
	            		isPerson = 0
	        else:
	        # Person is still standing in front of sensor
	            continue
		#END OF LOOP
	
 	#data = raw_input('Enter message to Server:')#'Station Current Total'#getdata()
	
def sendData(soc, host, port, Station, masterCount, previousTotal):
	# Creating message
	previousTimeCount = masterCount - previousTotal
	msg = Station + " {} {} ".format(previousTimeCount, masterCount)
	print "Sending: ", msg
	# Send Data
	while True:
		try:
        		bits_written = soc.send(msg)#write(data)
			print "data sent"
			break
		except:
			print "Connection broket"
			soc.close()
			soc = connectToServer(host, port)
			
	T = datetime.datetime.time(datetime.datetime.now())
	return [masterCount, T]
	
def cleanup(soc, Counter):
    # Close GPIO
    Counter.close()

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

def scheduleShutdown(file):
    	print "Schedule Shutdown"
	fid = open(file,"r")
        data = fid.read()
	datasplit = data.split()
	T = datetime.datetime.time(datetime.datetime.today())
	count = 1	

	for i in xrange(len(datasplit)):
		with Switch(datasplit[i]) as case:
			if case('M:') and datetime.datetime.today().weekday() == 0:
				while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
                                        count = count + 1
                                timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
			if case('T:') and datetime.datetime.today().weekday() == 1:
				while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
                                        count = count + 1
                                timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
			if case('W:') and datetime.datetime.today().weekday() == 2:
				while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
                                        count = count + 1
                                timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
			if case('t:' )and datetime.datetime.today().weekday() == 3:
				while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
                                        count = count + 1
                                timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
			if case('F:') and datetime.datetime.today().weekday() == 4:
				while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
                                        count = count + 1
                                timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
			if case('S:') and datetime.datetime.today().weekday() == 5:
				while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
                                        count = count + 1
                                timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
			if case('s:') and datetime.datetime.today().weekday() == 6:
				while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
                                        count = count + 1
                                timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))

		

	return timeRed

##########################################################################################	
##################################### New Main ###########################################
##########################################################################################

# Read initialization file
filePath = "/home/pi/Documents/Python/PeopleTracker-C4C/mainCode/initializationFile"

# Initalize Client
[soc, Counter, tol_dist, delay, station, host, port, personDelay] = init_client(filePath)
runClient(soc, Counter, tol_dist, delay, station, host, port, personDelay)
cleanup(soc, Counter)



