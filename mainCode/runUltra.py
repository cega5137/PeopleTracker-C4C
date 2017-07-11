print "Register GPIO"
import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

print "Starting Application"
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
t_start = time.time()
t_actual = t_start
n = 1
update_time = 1 # minutes

# Open File
now = datetime.datetime.now()
s = "/home/pi/WRTG_Proj/pi_counter_%d_%d_%d_%d.txt" % (now.month, now.day, now.year, now.minute)

FID = open(s, 'a', 0)
s = "Date: %d/%d/%d  %d:%d:%d" % (now.month, now.day, now.year,now.hour, now.minute, now.second)

FID.write(s)
s ="\tTime [min] \t\t Count update \t\t Total Count \t Minute Update time %d [minutes]\n" % update_time
FID.write(s)

#Start of Loop
while 1:
    t_actual = time.time()
    if t_actual - t_start >= (update_time * 60) * n:
        n = n + 1
        previousTimeCount = masterCount - previousTimeCount;
        #Print previousTimeCount and masterCount to file
        s ="\t\t\t\t%d \t\t\t %d \t\t\t %d\n" % ((t_actual-t_start)/60,  previousTimeCount, masterCount)
        FID.write(s)
        previousTimeCount = masterCount

    print "Begining of Main Loop"
    print "count = ", masterCount
    time.sleep(0.2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    
    distance = round(distance, 2)
    
    if distance > 400:
        continue

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

# Clean up
FID.close()
print "Ending Application"
GPIO.cleanup()
