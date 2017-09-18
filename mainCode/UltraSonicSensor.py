import RPi.GPIO as GPIO 
from time import sleep, time 
import multiprocessing
from interruptingcow import timeout

class UltraSonic():
	def __init__(self, Trig, Echo):
		GPIO.setmode(GPIO.BCM)
		self.TRIG = Trig #23
		self.ECHO = Echo #24

		GPIO.setup(self.TRIG, GPIO.OUT)
		GPIO.setup(self.ECHO, GPIO.IN)
		GPIO.output(self.TRIG, False)

		#self.q = multiprocessing.Queue()
		#self.p = multiprocessing.Process(target=self.runUltraSensor, name="runUltraS", args=())
		#sleep(1)

	def getDistance(self):
#		self.p.start()
#		distance = self.q.get()
#		self.p.join(2)
		print "distance inside: ", distance[0] 
	

#		if self.p.is_alive():
#			print "Function is running over time ... killing it"
#			self.p.terminate()
#			self.p.join()

		return distance[0]

	def runUltraSensor(self):
		try:
			with timeout(5, exception=RuntimeError):
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
				sleep(11)
				#self.q.put([distance])
		except RuntimeError:
			print "Took longer than 5 seconds"

	def close(self):
		GPIO.cleanup()
#		self.p.join()
		
		
if __name__ == "__main__":
	sensor = UltraSonic(23,24)
	d = sensor.runUltraSensor()
	print "Distance is: ", d 
	sensor.close()
	
