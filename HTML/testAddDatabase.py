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
from switch import Switch
#import Adafruit_DHT


def log_values(Header, currn, total):
	
	conn=sqlite3.connect('/var/www/html/PeopleTracker-C4C/HTML/mainDatabase.db')  #It is important to provide an
							     #absolute path to the database
							     #file, otherwise Cron won't be
							     #able to find it!
	curs=conn.cursor()
	print Header, currn
	with Switch(Header) as case:
		if case("Asian"):
			curs.execute('''INSERT INTO Asian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total))
		if case("American"):
			curs.execute('''INSERT INTO American values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total))
		if case("Persian"):
			curs.execute('''INSERT INTO Persian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total))
		if case("Italian"):
			curs.execute('''INSERT INTO Italian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total))
		if case("Latin"):
			curs.execute('''INSERT INTO Latin values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total))

#	switcher = {
#		'Asian': curs.execute('''INSERT INTO Asian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total)),
#		'American': curs.execute('''INSERT INTO American values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total)),
#		'Persian':curs.execute('''INSERT INTO Persian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total)),
#		'Italian':curs.execute('''INSERT INTO Italian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total)),
#		'Latin':curs.execute('''INSERT INTO Latin values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total)),
#
#	}
#	return switcher.get(Header,"Nothing")

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
#from socket import *
import time
import datetime

print "Startin application"

humidity = random.randint(1,100)
temperature = random.randint(10,70)

As = random.randint(1,100)
log_values('Asian', As, As)
Am = random.randint(1,100)	
log_values("American", Am, Am)
Pe = random.randint(1,100)
log_values("Persian", Pe, Pe)
It = random.randint(1,100)
log_values("Italian", It, It)
La = random.randint(1,100)
log_values("Latin", La, La)

