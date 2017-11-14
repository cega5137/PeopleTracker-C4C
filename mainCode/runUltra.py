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
        for i in [0,2,4,6,8,10, 12, 14]:
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
			if case('shutdownCase:'):
				shutdownSwitch = bool(int(dataSplit[i+1]))


        return [Station, ipaddr, port, delayTime, TRIG, ECHO, tol_dist, waitPerson, shutdownSwitch]

def init_client(initializationFile):
    #Get the initialization file
	[Station, host, port, sendingDelay, TRIG, ECHO, tol_dist, personDelay, shutdownSwitch] = readInitialization(initializationFile)
	Counter = UltraSonic(TRIG,ECHO)
	print Station
	print host
	print port
	
    # Initializes the client
	#signal.signal(signal.SIGPIPE, signal.SIG_IGN)
    
    	return [connectToServer(host, port), Counter, tol_dist, sendingDelay, Station, host, port, personDelay, shutdownSwitch]

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

def runClient(soc, Counter, tol_dist, sendingDelay, station, host, port, personDelay, shutdownSwitch, onFile, offFile):
	#set up variable declaration
	[masterCount, previousTotal, isPerson, t_actual] = variableDeclaration()
	
	#Schedule shutdown
	print "Getting shutdown time"
	schShut = scheduleShutdown(offFile) 

	#Main Loop
	while True:
        # Take Measurment
		T = datetime.datetime.time(datetime.datetime.now())
		if T >= schShut:
			# Check if needs to turn off
			if shutdownSwitch:
			# break if it does
				break
			schShut, soc, Counter, host, port, station = standbyRun(soc, Counter, onFile, offFile)
			# get on standby funtion
			# get new schShut

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
	
def cleanup(soc, Counter, switchOff):
    # Close GPIO
    Counter.close()

    # Close Socket
    if (soc > 0):
        soc.close()
    # Shutdown pi
    if switchOff:
    	shutdownRPi()

def shutdownRPi():
    	print "Shutting down"
    	command = "/usr/bin/sudo /sbin/shutdown -h now"
    	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    	output = process.communicate()[0]
    	print output

def scheduleShutdown(file):
	fid = open(file,"r")
	data = fid.read()
	datasplit = data.split()
	T = datetime.datetime.time(datetime.datetime.today())
	dayWeek = datetime.datetime.today().weekday()
	count = 1	

	for i in xrange(len(datasplit)):
		
		with Switch(datasplit[i]) as case:
			if case('Mon:') and dayWeek == 0:
				try:
					while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
						count = count + 1
					timeRed = datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
				except:
					timeRed = datetime.time(int(datasplit[i+count+1][0:2]), int(datasplit[i+count+1][3:5]))
					#dayWeek = dayWeek + 1
					break

			if case('Tue:') and dayWeek == 1:
				try:
					while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
						count = count + 1
					timeRed = datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
				except:
					timeRed = datetime.time(int(datasplit[i+count+1][0:2]), int(datasplit[i+count+1][3:5]))
					#dayWeek = dayWeek + 1
					break

			if case('Wen:') and dayWeek == 2:
				try:
					while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
						count = count + 1
					timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
				except:
					timeRed = datetime.time(int(datasplit[i+count+1][0:2]), int(datasplit[i+count+1][3:5]))
					#dayWeek = dayWeek + 1
					break

			if case('Thu:' )and dayWeek == 3:
				try:
					while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
						count = count + 1
					timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
				except:
					timeRed = datetime.time(int(datasplit[i+count+1][0:2]), int(datasplit[i+count+1][3:5]))
					#dayWeek = dayWeek + 1
					continue

			if case('Fri:') and dayWeek == 4:
				try:
					while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
						count = count + 1
					timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
				except:
					timeRed = datetime.time(int(datasplit[i+count+1][0:2]), int(datasplit[i+count+1][3:5]))
					#dayWeek = dayWeek + 1
					continue

			if case('Sat:') and dayWeek == 5:
				try:
					while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
						count = count + 1
					timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
				except:
					timeRed = datetime.time(int(datasplit[i+count+1][0:2]), int(datasplit[i+count+1][3:5]))
					#dayWeek = dayWeek + 1
					continue

			if case('Sun:') and dayWeek == 6:
				try:
					while datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5])) < T:
						count = count + 1
					timeRed =  datetime.time(int(datasplit[i+count][0:2]),int(datasplit[i+count][3:5]))
				except:
					#timeRed = datasplit[i+count+1]
					#dayWeek = 0
					timeRed =  datetime.time(int(datasplit[2][0:2]),int(datasplit[2][3:5]))

	return timeRed


def standbyRun(soc, Counter, onFile, offFile):
	# Check when it needs to turn on
	print "getting on time"
	onStart = scheduleShutdown(onFile) # On file
	
	#Close connection and GPIO
	cleanup(soc, Counter, False)
	
	print "Waking up at: ", onStart
	# Do the wait
	T = datetime.datetime.time(datetime.datetime.now())
	while T >= onStart:
		time.sleep(60*15)
		T = datetime.datetime.time(datetime.datetime.now())

	# check new time to turn off
	print "getting off time"
	offStart = scheduleShutdown() # Off file

	# initialize code again
	[soc, Counter, tol_dist, delay, station, host, port, personDelay] = init_client(filePath)
	return offStart

##########################################################################################	
##################################### New Main ###########################################
##########################################################################################

# Read initialization file
filePath = "/home/pi/Documents/Python/PeopleTracker-C4C/mainCode/initializationFile.ini"
onFile = "/home/pi/Documents/Python/PeopleTracker-C4C/mainCode/startTime.ini"
offFile = "/home/pi/Documents/Python/PeopleTracker-C4C/mainCode/shutdownTime.ini"

# Initalize Client
[soc, Counter, tol_dist, delay, station, host, port, personDelay, shutdownSwitch] = init_client(filePath)
runClient(soc, Counter, tol_dist, delay, station, host, port, personDelay, shutdownSwitch, onFile, offFile)
cleanup(soc, Counter, True)



