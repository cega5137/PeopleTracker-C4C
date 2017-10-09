import socket 
import random
import time
from threading import Thread

#
class ClientThread(Thread):
	def __init__(self, ip, port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		print "[+] New server socket thread started for " + ip + ":" + str(port)

	def run(self):
		while True :
			data = conn.recv(2028)
			print "Server received data: ", data
			#time.sleep(1)
#			MSG = raw_input("Multithreaded Python Server:")
			#if MSG == 'exit':
			#	break
			#conn.send(MSG)

# Multithreaded Python server
TCP_IP = '10.0.0.150'
TCP_PORT = 2004
BUFFER_SIZE = 1024

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
	tcpServer.listen(4)
	print "MultThreaded Python Server: Waiting for connection from TCP clients"
	(conn, (ip, port)) = tcpServer.accept()
	newthread = ClientThread(ip, port)
	newthread.start()
	threads.append(newthread)

for t in threads:
	t.join()


'''
host = "10.0.0.151" # ip address of the server

print host

port = 4447

s = socket(AF_INET, SOCK_STREAM)

print "Socket Made"

s.bind((host, port))

print "Socket Bound"


s.listen(5)

print "Listening for connection..."

q, addr= s.accept()
print "Connected to address: ", addr
w, addr2=s.accept()
print "Connected to addres: ", addr2

clientN1 = q.recv(1024)
print "who is on? ", clientN1
q.send("Thank you for connecting")

clientN2 = w.recv(1024)
print "who is on? ", clientN2
w.send("Thank you for connection")


try:
	while True:
		msg1 = q.recv(1024)
		print "Sending Original mesage: ", msg1
		msgBack1 = msg1 + " Got your message Client"
		q.send(msgBack1)

		msg2 = w.recv(1024)
		print "Sending Original mesage: ", msg2
                msgBack2 = msg2 + " Got your message Client"
                w.send(msgBack2)		

except KeyboardInterrupt: 
	print "Closing connection"
	s.close

## define Thread function
def recvSendMsg(Channel):
	msg = Channel.recv(1024)
	print "Sending Original mesage: ", msg
        msgBack = msg + " Got your message Client"
        Channel.send(msgBack)

'''
