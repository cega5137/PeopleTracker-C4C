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


def log_values(Header, currn, total):
	conn=sqlite3.connect('/var/www/html/mainDatabase.db')  #It is important to provide an
							     #absolute path to the database
							     #file, otherwise Cron won't be
							     #able to find it!
	curs=conn.cursor()
	
	switcher = {
		'Asian': curs.execute('''INSERT INTO Asian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total)),
		'American': curs.execute('''INSERT INTO American values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total)),
		'Persian':curs.execute('''INSERT INTO Persian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total)),
		'Italian':curs.execute('''INSERT INTO Italian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total)),
		'Latin':curs.execute('''INSERT INTO Latin values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total)),

	}
	return switcher.get(Header,"Nothing")

#	curs.execute('''INSERT INTO temperatures values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (sensor_id,temp))
#	curs.execute('''INSERT INTO humidities values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (sensor_id,hum))
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


print "Startin application"

host = "10.0.0.227"
port = 4446
s=socket(AF_INET,SOCK_STREAM)

print "Done set up port and host"
while True:
	while True:
		try:
			s.connect((host, port))
			print "Connecting ..."
			break
		except:
			print "Waiting for message..."
			time.sleep(1)


	msg=s.recv(1024)
	print "Message receive"
	print "Number of People " + msg

#	s.close
	
	time.sleep(1)
	s=socket(AF_INET,SOCK_STREAM)

	data = msg.split(" ")

	header = data[0]

	curr = int(data[1])

	Total = int(data[2])


	humidity = random.randint(1,100)
	temperature = random.randint(10,70)

	if curr is not None and Total is not None:
		log_values(header, curr, Total)	
	else:
		log_values(header, -999, -999)
