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
from threading import Thread
from SocketServer import ThreadingMixIn
from switch import Switch

class ClientThread(Thread):
        def __init__(self, ip, port):
                Thread.__init__(self)
                self.ip = ip
                self.port = port
                print "[+] New server socket started for " + ip + ": " + str(port)

        def run(self):
                while True:
                        msg = conn.recv(2048)
                        print "Server receive data: ", msg
			print "At :", datetime.datetime.time(datetime.datetime.now())
			data = msg.split(" ")
			if len(data) == 2:
				header = data[0]
				curr = int(data[1])
				Total = int(data[2])
				if curr is not None and Total is not None:
					self.log_values(header, curr, Total)
				else: 
					self.log_values(header, -999, -999)

                        	MSG = "ON"
                        	conn.send(MSG)

			else:
				MSG = "OFF"
				conn.send(MSG)

	
	def log_values(self, Header, currn, total):
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

#humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
#temperature = temperature * 9/5.0 + 32
# If you don't have a sensor but still wish to run this program, comment out all the 
# sensor related lines, and uncomment the following lines (these will produce random
# numbers for the temperature and humidity variables):
import random

####################################################
print "Startin application"

hostIP = "10.0.0.150"
port = 3333
BUFFER_SIZE = 20

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((hostIP,port))
threads = []
#s=socket(AF_INET,SOCK_STREAM)
#i = 0

print "Done set up port and host"
while True:
	tcpServer.listen(5)
	print "Waiting connection from clients"
	(conn, (ip, port)) = tcpServer.accept()
	newthread = ClientThread(ip, port)
	newthread.start()
	threads.append(newthread)
		
	for t in threads:
		print "In the for loop"
		t.join()






#	while True:
#		try:
#			s.connect((host, port))
#			print "Connecting ..."
#			break
#		except:
#			print "Waiting for message..."
#			time.sleep(1)


#	msg=s.recv(1024)
#	print "Message receive"
#	print "Number of People " + msg
#	i = i + 1
#	print "Counting i = ", i, "at ", datetime.datetime.now()

#	s.close
	
#	time.sleep(1)
#	s=socket(AF_INET,SOCK_STREAM)

#	data = msg.split(" ")

#	header = data[0]
#	curr = int(data[1])
#	Total = int(data[2])

#	if curr is not None and Total is not None:
#		log_values(header, curr, Total)	
#	else:
#		log_values(header, -999, -999)
