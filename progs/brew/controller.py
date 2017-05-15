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
#GPIO.output(11, False) # heater
#GPIO.output(13, False) # pump
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# make a path to the file where sensor data resides 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-0216148d2eee')[0]
device_file = device_folder + '/w1_slave'
 
# mash variables
pump_duty_cycle = [True,True,True,True,True] # on for all cycles
temp_offset1 = 0.0 #-0.3	# error in reading
debug_mode = True	# show messages or not

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
	

def print_stuff(s):
	if debug_mode:
		print "temp = ", s.hold_temp, "mash time = ", s.hold_time, "pump setting = ", (s.pdc), "%"


def map_pid(pid_val, herms, last_herms, heater):

	pid_max = 8
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

#	if pid_val > 10:
#		heater.ChangeDutyCycle(100)
#		return
#	if pid_val > 8:
#		heater.ChangeDutyCycle(80)
#		return
#	if pid_val > 6:
#		heater.ChangeDutyCycle(60)
#		return
#	if pid_val > 4:
#		heater.ChangeDutyCycle(40)
#		return
#	if pid_val > 0:
#		heater.ChangeDutyCycle(20)
#		return	
#	else:
#		heater.ChangeDutyCycle(0)


try:	
	if debug_mode:
		print "Starting..."
	else:
		file = open("results.txt",'w')


	
	# initialize system
	s = Settings()
	p = PID( s.p, s.i , s.d) # original settings 3.0,0.4,1.2
	p.setPoint(s.hold_temp)
	print_stuff(s)
	#pump = GPIO.PWM(13,0.1) 	# 10 seconds / cycle
	heater = GPIO.PWM(11,10) 	# 10 Hz 

	#pump.start(s.pdc)
	heater.start(0)

	#pump.ChangeDutyCycle(75)

	# initialize loop variables
        i = 0
	start = time.time()
	dt = 0
	last_herms = 0
        herms = read_temp()

        while dt < float(s.hold_time * 60):

		dt = time.time() - start
		last_herms = herms
        	herms = read_temp()
		pid = p.update(herms)
		i += 1
        	

		#Control section------------------------------------------------------------

		map_pid(pid, herms, last_herms, heater)

		#---------------------------------------------------------------------------
				
		if debug_mode:
			print herms + temp_offset1, ",", round( dt, 2 ), ",", round( pid,3 )


except KeyboardInterrupt:
	if debug_mode:
    		print "\n ***** Exiting Program *****"
except:
	if debug_mode:
	   	print "\n ***** PROGRAMMATIC FAILURE *****"
finally:
	GPIO.cleanup()
	if debug_mode:
		print "finished"
	


