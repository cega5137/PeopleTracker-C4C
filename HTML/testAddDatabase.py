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
	conn.commit()
	conn.close()

def addingTest():
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


def getDay(station, dayToday):
	conn = sqlite3.connect("/var/www/html/PeopleTracker-C4C/HTML/mainDatabase.db"
	curs = conn.cursor()
	
	with Switch(Station) as case:
		


import random
#from socket import *
import time
import datetime

print "Startin application"


print "End application"
