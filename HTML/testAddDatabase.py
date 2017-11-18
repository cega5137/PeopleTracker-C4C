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
import datetime
import time
import numpy as np
#import Adafruit_DHT
from random import randint
#from socket import *
#import time
#import datetime


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

def createDatabase():
	conn=sqlite3.connect("C:/User/cesar/Documents/Projects/testDatabase.db")
	
	curs=conn.cursor()
	curs.execute('''CREATE TABLE Persian (date text, curr, Total)''')
	curs.execute('''CREATE TABLE Asian (date text, currn, Total)''')
	curs.execute('''CREATE TABLE American (date text, currn, Total)''')
	curs.execute('''CREATE TABLE Latin (date text, currn, Total)''' )
	curs.execute('''CREATE TABLE Italian (date text, currn, Total)''' )

	conn.commit()
	conn.close()

def sampleData(station, fromDate, toDate):
	conn = sqlite3.connect("C:/User/cesar/Documents/Projects/testDatabase.db")
	curs = conn.cursor()

	minutes = [00, 15, 30, 45]
	hours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
	dateCurrent = fromDate
	Data = []

	while dateCurrent < toDate:
		for timeHour in hours:
			for timeMinute in minutes:
				if timeHour == 20 and timeMinute != 0:
					continue
				log_date = datetime.datetime(dateCurrent.year, dateCurrent.month, dateCurrent.day, timeHour, timeMinute)
				print log_date
				Data.append([log_date, randint(0,100), randint(0,500)])
		try: 
			dateCurrent = datetime.datetime(dateCurrent.year, dateCurrent.month, dateCurrent.day+1)
		except:
			try:
				dateCurrent = datetime.datetime(dateCurrent.year, dateCurrent.month+1, 1)
			except:
					dateCurrent = datetime.datetime(dateCurrent.year+1, 1, 1)

	with Switch(Station) as case:
		if case('Asian'):
			curs = exceutemany('INSERT INTO Asian VALUES (?,?,?)', Data)
		
		if case('American'):
			curs = exceutemany('INSERT INTO American VALUES (?,?,?)', Data)
			
		if case('Persian'):
			curs = exceutemany('INSERT INTO Persian VALUES (?,?,?)', Data)

		if case('Italian'):
			curs = exceutemany('INSERT INTO Italian VALUES (?,?,?)', Data)

		if case('Latin'):
			curs = exceutemany('INSERT INTO Latin VALUES (?,?,?)', Data)

	conn.commit()
	conn.close()	

def getDay(station, fromDate, toDate):
	conn = sqlite3.connect("C:/User/cesar/Documents/Projects/testDatabase.db")
	curs = conn.cursor()

	with Switch(Station) as case:
		if case('Asian'):
			curs.execute("SELECT * FROM Asian WHERE date BETWEEN ? AND ?", (fromDate.format('YYYY-MM-DD HH:mm'), toDate.format('YYYY-MM-DD HH:mm')))
			#curs.execute("SELECT * FROM Asian")
			data = curs.fetchall()
		if case('American'):
			curs.execute("SELECT * FROM American WHERE date BETWEEN ? AND ?", (fromDate.format('YYYY-MM-DD HH:mm'), toDate.format('YYYY-MM-DD HH:mm')))
			#curs.execute("SELECT * FROM American")
			data = curs.fetchall()
		if case('Persian'):
			curs.execute("SELECT * FROM Persian WHERE date BETWEEN ? AND ?", (fromDate.format('YYYY-MM-DD HH:mm'), toDate.format('YYYY-MM-DD HH:mm')))
			#curs.execute("SELECT * FROM Persian")
			data = curs.fetchall()
		if case('Italian'):
			curs.execute("SELECT * FROM Italian WHERE date BETWEEN ? AND ?", (fromDate.format('YYYY-MM-DD HH:mm'), toDate.format('YYYY-MM-DD HH:mm')))
			#curs.execute("SELECT * FROM Italian"),
			data = curs.fetchall()
		if case('Latin'):
			curs.execute("SELECT * FROM Latin WHERE date BETWEEN ? AND ?", (fromDate.format('YYYY-MM-DD HH:mm'), toDate.format('YYYY-MM-DD HH:mm')))
			#curs.execute("SELECT * FROM Latin")
			data = curs.fetchall()

	#print "Data: ", data[0][0]

	hourInDay = ['7','8','9','10','11','12','13','14','15','16','17','18','19','20']
	Time = np.zeros([24, 7, 10])
	timeIndex = np.zeros([24,7])
	t0 = time.time()
	previousDate = None
	for Data in data:
		#Check day of the week for each entry
		#print "Data", Data
		#print Data[0][11:13] # Hour
		week = datetime.date(int(Data[0][0:4]),int(Data[0][5:7]),int(Data[0][8:10])).weekday()
		timeOfDay = int(Data[0][11:13])
		#print week, timeOfDay, Data[1]
		
		# Save data on matrix
		Time[timeOfDay][week][timeIndex[timeOfDay][week]] = Time[timeOfDay][week][timeIndex[timeOfDay][week]] + Data[1]
		print Time[timeOfDay][week][timeIndex[timeOfDay][week]]
		
		if previousDate != Data[0][0:10] and previousDate != None:
			#print "Time: ", previousTime
			#print "Week: ", previousWeek
			timeIndex[previousTime][previousWeek] = timeIndex[previousTime][previousWeek] + 1  
		
		previousDate = Data[0][0:10]
		previousTime = timeOfDay
		previousWeek = week

	tf = time.time()
	print "It takes:", tf - t0
	return Time, timeIndex

def getDayCount(Data, week):
	hourInDay = ['7','8','9','10','11','12','13','14','15','16','17','18','19','20']
	for dayofWeek in xrange(0,7):
                        for hourofDay in hourInDay:
                                if week == dayofWeek and Data[0][11:13] == hourofDay:
                                        #print "it work!!", week, Data[0][11:13]
                                        return Data[1], hourofDay

	return None


def getTimeDate(Data):
	with Switch(Data) as case:
		if case('7'):
			return 7
		if case('8'):
			return 8
		if case('9'):
			return 9
		if case('10'):
			return 10
		if case('11'):
			return 11
		if case('12'):
			return 12
		if case('13'):
			return 13
		if case('14'):
			return 14
		if case('15'):
			return 15
		if case('16'):
			return 16
		if case('17'):
			return 17
		if case('18'):
			return 18
		if case('19'):
			return 19
		if case('20'):
			return 20




if __name__ == '__main__':
	print "Startin application"
	createDatabase()
	#American = getDay('American')
	#Asian =  getDay('Asian')
	#Latin = getDay('Latin')
	#Persian = getDay('Persian')
	#Italian = getDay('Italian')
	startDate = datetime.datetime(2017,9,01,00,00)
	endDate = datetime.datetime(2017,12,01,20,00)
	sampleData('American',startDate, endDate)
	sampleData('Asian',startDate, endDate)
	sampleData('Latin',startDate, endDate)
	sampleData('Persian',startDate, endDate)
	sampleData('Italian',startDate, endDate)

	print "End application"
