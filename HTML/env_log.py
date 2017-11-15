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
import socket
import time
import datetime
from threading import Thread, activeCount
from SocketServer import ThreadingMixIn
from switch import Switch
import signal

class client_thread(Thread):
	def __init__(self, clientsocket, ip, port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.bufferSize = 1024
		self.conn = clientsocket
		print "[+] New server socket started for " + ip + ": " + str(port)
		print "The Thread Count is: ", activeCount()

	def run(self):
		# Setting up the prevoius time 
		firstRun = True
		
		while True:
			msg = self.conn.recv(self.bufferSize)
			print "Server receive data: ", msg
			T = datetime.datetime.time(datetime.datetime.now())
			print "At :", T
			data = msg.split(" ")
			header = data[0]
			curr = int(data[1])
			Total = int(data[2])
			
			if curr is not None and Total is not None:
				if firstRun:
					self.log_values(header,curr, Total)
					firstRun = False
					previousT = datetime.datetime.time(datetime.datetime.now())

				if not T.minute == previousT.minute: 
					self.log_values(header, curr, Total)
					previousT = datetime.datetime.time(datetime.datetime.now())
					firstRun = False
			else: 
				self.log_values(header, -999, -999)
			MSG = "ON"
	#                      	conn.send(MSG)

	#			except:
	#				MSG = "OFF"
	#				conn.send(MSG)
			
	
	def log_values(self, Header, currn, total):
		#conn=sqlite3.connect('C:\User\cesar\Documents\Projects\PeopleTracker-C4C\HTML\mainDatabase.db')
		conn=sqlite3.connect('/var/www/html/PeopleTracker-C4C/HTML/mainDatabase.db')  #It is important to provide an
                	                                             #absolute path to the database
                        	                                     #file, otherwise Cron won't be
                                	                             #able to find it!
		curs=conn.cursor()	
	
		with Switch(Header) as case:
			if case('Asian'):
				curs.execute('''INSERT INTO Asian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total))
				print "Saving current and total in Asian: ", currn, ", ", total
			if case('American'):
				curs.execute('''INSERT INTO American values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total))
				print "Saving current and total in American: ", currn, ", ", total

			if case('Persian'):
				curs.execute('''INSERT INTO Persian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total))
				print "Saving current and total in Persian: ", currn, ", ", total

			if case('Italian'):
				curs.execute('''INSERT INTO Italian values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total))
				print "Saving current and total in Italian: ", currn, ", ", total

			if case('Latin'):
				curs.execute('''INSERT INTO Latin values(datetime(CURRENT_TIMESTAMP, 'localtime'), (?), (?))''', (currn,total))
				print "Saving current and total in Latin: ", currn, ", ", total

			conn.commit()
			conn.close()

def init(host, Port):
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serversocket.bind((host, Port))
	serversocket.listen(5)
	signal.signal(signal.SIGPIPE, signal.SIG_IGN) # Off for windows
	return serversocket
	
def run(serversocket, host, port):
	threads = []
	while 1:
		print "Waiting for connections"
		(clientsocket, address) = serversocket.accept()
		ct = client_thread(clientsocket, host, port)
		ct.start()
		threads.append(ct)
		
	for t in threads:
		t.join()
		
def cleanup(serversocket):
	serversocket.close()
	print "Closing Connection"

####################################################
print "Startin application"
#hostIP = "10.202.18.51"
hostIP = "10.0.0.227"
port = 5003
serversocket = init(hostIP, port)
run(serversocket, hostIP, port)
cleanup()
