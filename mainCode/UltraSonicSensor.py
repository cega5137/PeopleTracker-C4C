import RPi.GPIO as GPIO 
from time import sleep 


class UltraSonic():
	def __init__(self, Trig, Echo):
		GPIO.setmode(GPIO.BCM)
		self.TRIG = Trig #23
		self.ECHO = Echo #24

		GPIO.setup(TRIG,GPIO.OUT)
		GPIO.setup(ECHO,GPIO.IN)
		GPIO.output(TRIG, False)
		sleep(2)

	def getDistance(self):
		sleep(0.2)
	    GPIO.output(self.TRIG, True)
	    sleep(0.00001)
	    GPIO.output(self.TRIG, False)

	    	while GPIO.input(self.ECHO)==0:
	        	pulse_start = time.time()

			while GPIO.input(self.ECHO)==1:
		        pulse_end = time.time()
				
		pulse_duration = pulse_end - pulse_start

	    distance = pulse_duration * 17150
	    
	    distance = round(distance, 2)
	    
	    return distance

	def close():
		GPIO.cleanup()
		
		
if __name__ == __main__:
	sensor = UltraSonic(23,24)
	d = sensor.getDistance()
	print "Distance is: ", d 