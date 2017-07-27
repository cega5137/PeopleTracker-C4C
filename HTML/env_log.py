#!/usr/bin/env python


# To do list:
# Check to see who is sending the message
# 

'''
FILE NAME
env_log.py
1. WHAT IT DOES
Takes a reading from a DHT sensor and records the values in an SQLite3 database using a Raspberry Pi.
 
2. REQUIRES
* Any Raspberry Pi
* A DHT sensor
* A 10kOhm resistor
* Jumper wires
3. ORIGINAL WORK
Raspberry Full stack 2015, Peter Dalmaris
4. HARDWARE
D17: Data pin for sensor
5. SOFTWARE
Command line terminal
Simple text editor
Libraries:
import sqlite3
import sys
import Adafruit_DHT
6. WARNING!
None
7. CREATED 
8. TYPICAL OUTPUT
No text output. Two new records are inserted in the database when the script is executed
 // 9. COMMENTS
--
 // 10. END
'''



import sqlite3
import sys
#import Adafruit_DHT

def log_values(sensor_id, temp, hum):
	conn=sqlite3.connect('/var/www/html/lab_app.db')  #It is important to provide an
							     #absolute path to the database
							     #file, otherwise Cron won't be
							     #able to find it!
	curs=conn.cursor()
	
	curs.execute('''INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (sensor_id,temp))
	curs.execute('''INSERT INTO humidities values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (sensor_id,hum))
	conn.commit()
	conn.close()

#humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
#temperature = temperature * 9/5.0 + 32
# If you don't have a sensor but still wish to run this program, comment out all the 
# sensor related lines, and uncomment the following lines (these will produce random
# numbers for the temperature and humidity variables):
import random
from socket import *
import time

host = "10.0.0.227"
port = 4446
s=socket(AF_INET,SOCK_STREAM)
while True:
	while True:
		try:
			s.connect((host, port))
			break
		except:
			print "Waiting for message..."
			time.sleep(1)


	msg=s.recv(1024)
	print "Message receive"
	print "Nnumber of Poeple " + msg

	s.close
	
	time.sleep(1)
	s=socket(AF_INET,SOCK_STREAM)

	data = msg.split(" ")

	curr = int(data[0])

	Total = int(data[1])


	humidity = random.randint(1,100)
	temperature = random.randint(10,70)

	if humidity is not None and temperature is not None:
		log_values("1", curr, Total)	
	else:
		log_values("1", -999, -999)
