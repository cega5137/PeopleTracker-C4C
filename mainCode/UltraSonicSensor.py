import RPi.GPIO as GPIO 
from time import sleep, time 
from interruptingcow import timeout

class UltraSonic():
	def __init__(self, Trig, Echo):
		GPIO.setmode(GPIO.BCM)
		self.TRIG = Trig #23
		self.ECHO = Echo #24

		GPIO.setup(self.TRIG, GPIO.OUT)
		GPIO.setup(self.ECHO, GPIO.IN)
		GPIO.output(self.TRIG, False)

	def getDistance(self):
		try:
			with timeout(2, exception=RuntimeError):
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
				return distance

		except RuntimeError:
			print "Took longer than 5 seconds"
			pass
		except UnboundLocalError:
			print "Unbound Error"
			pass

	def close(self):
		GPIO.cleanup()
		
if __name__ == "__main__":
	sensor = UltraSonic(23,24)
	d = sensor.getDistance()
	print "Distance is: ", d 
	sensor.close()
	
