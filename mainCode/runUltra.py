print "Register GPIO" 
import RPi.GPIO as GPIO 
import time 
import datetime 
import socket

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

print "Starting Application..."
time.sleep(2)

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
host = "10.0.0.151"
port = 3333
BUFFER_SIZE = 2000
Sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Sc.connect((host, port))

#Start of Loop
try:
	while 1:
    		print "Getting the time"
    		T = datetime.datetime.time(datetime.datetime.now())

    		if  (T.microsecond/1000) < 300 and T.minute == 0 or T.minute == 15 or T.minute == 30 or T.minute == 45:
			n = n + 1
        		previousTimeCount = masterCount - previousTimeCount;
			print "Saving time is: ", T

        		#### Sending data
			msg = "American {} {} ".format(previousTimeCount, masterCount)
			Sc.send(msg)
			State = Sc.recv(BUFFER_SIZE)
			print "Raspberry pi State: ", State
			previousTimeCount = masterCount
			T = datetime.datetime.time(datetime.datetime.now())	
			print "End of the if statement"

    		print "Begining of Main Loop", T
    		print "count = ", masterCount
    		time.sleep(0.2)
    		GPIO.output(TRIG, True)
    		time.sleep(0.00001)
    		GPIO.output(TRIG, False)

    		while GPIO.input(ECHO)==0:
        		pulse_start = time.time()

    
    		while GPIO.input(ECHO)==1:
        		pulse_end = time.time()
	
#    		print "Pulse Start", pulse_start
#    		print "Pulse End: ", pulse_end
    		pulse_duration = pulse_end - pulse_start

    		distance = pulse_duration * 17150
    
    		distance = round(distance, 2)
    
    		if distance > 400:
        		continue

		#Commenting line
    		print "Distance:",distance,"cm"
    		#    print "isPerson:", isPerson, "tol_dist =", tol_dist
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

except KeyboardInterrupt:
	# Clean up
	print "Cleaning up \nEnding Application"
	GPIO.cleanup()
