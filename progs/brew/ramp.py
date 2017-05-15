from pid import PID
from settings import Settings
import os
import sys
import glob
import time
import RPi.GPIO as GPIO

# setup the gpio and sensor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_offset1 = -0.3	# error in reading
debug_mode = True	# show messages or not
time_max = 30
temp_hold = 70

def read_temp_raw():

	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28-0216148d2eee')[0]
	device_file = device_folder + '/w1_slave'

	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines


def read_temp():

	lines = read_temp_raw()

	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equal_pos = lines[1].find('t=')
	if equal_pos != -1:
		temp_string = lines[1][equal_pos+2:]
		temp_c = round(float(temp_string) / 1000.0, 1)
		return temp_c +temp_offset1 
	

def map_pid(pid_val,heater):

	pid_max = 5
	ratio = pid_val / pid_max

	if ratio > 1.0 :

                heater.ChangeDutyCycle(100)
		return

	elif ratio > 0 :

                heater.ChangeDutyCycle( round( 100 * ratio ) )
		return
	else:
                heater.ChangeDutyCycle(0)
		return


try:	
	
	# initialize system
	s = Settings()
	p = PID(3.0,0.3,1.7) # original settings 3.0,0.4,1.2
	p.setPoint(temp_hold)

	#pump = GPIO.PWM(13,0.1) 	# 10 seconds / cycle
	heater = GPIO.PWM(11,10) 	# 10 Hz 

	#pump.start(s.pdc)
	heater.start(0)

	#pump.ChangeDutyCycle(75)

	# initialize loop variables
	start = time.time()
	dt = 0


        while dt < float( time_max * 60 ):

		dt = time.time() - start
        	herms = read_temp()
		pid = p.update(herms)
        	

		#Control section------------------------------------------------------------

		map_pid(pid, heater)

				
		if debug_mode:
			print herms + temp_offset1, ",", round(dt,2), ",", round(pid,3)

		#---------------------------------------------------------------------------


except KeyboardInterrupt:
	if debug_mode:
    		print "\n ***** Exiting Program *****"
except:
	if debug_mode:
	   	print "\n ***** PROGRAMMATIC FAILURE *****"
finally:
	GPIO.cleanup()
	


# Notes on pid tuning:
	# original settings 3 , 0.4, 1.2
	# next run 3, 0.3, 1.5
