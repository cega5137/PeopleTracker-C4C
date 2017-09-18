import RPi.GPIO as GPIO 
from time import sleep, time 
import multiprocessing

class UltraSonic():
	def __init__(self, Trig, Echo):
		GPIO.setmode(GPIO.BCM)
		self.TRIG = Trig #23
		self.ECHO = Echo #24

		GPIO.setup(self.TRIG, GPIO.OUT)
		GPIO.setup(self.ECHO, GPIO.IN)
		GPIO.output(self.TRIG, False)
		
		self.distance = None
		self.q = multiprocessing.Queue()
		self.p = multiprocessing.Process(target=self.runUltraSensor, name="runUltraS", args=())
		sleep(2)

	def getDistance(self):
		#q = multiprocessing.Queue()
		#p = multiprocessing.Process(target=self.runUltraSensor, name="runUltraS", args=(q,))
		self.p.start()
#		p.join()
		distance = self.q.get()

		print "distance inside: ", distance[0] 

#		p.terminate()
#		p.join()
		if self.p.is_alive():
			print "Function is running over time ... killing it"
			self.p.terminate()
			self.p.join()

		return distance[0]

	def runUltraSensor(self):
		sleep(0.2)
		GPIO.output(self.TRIG, True)
		sleep(0.00001)
		GPIO.output(self.TRIG, False)

	    	while GPIO.input(self.ECHO)==0:
	        	pulse_start = time()

		while GPIO.input(self.ECHO)==1:
		        pulse_end = time()
				
		pulse_duration = pulse_end - pulse_start
	
		distance = pulse_duration * 17150
	    
		distance = round(distance, 2)
	    	#self.distance = distance
		self.q.put([distance])

	def close(self):
		GPIO.cleanup()
		self.p.join()
		
		
if __name__ == "__main__":
	sensor = UltraSonic(23,24)
	d = sensor.getDistance()
	print "Distance is: ", d 
	sensor.close()
	
