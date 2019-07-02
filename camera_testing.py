##This is old code!! AVOID

import time
import RPi.GPIO as GPIO
from picamera import PiCamera
import os
from subprocess import check_output
from datetime import datetime
import numpy as np
from PIL import Image


GPIO.setwarnings(False)

i = 0
light = 12
#wifi = 7

ping_hub = "ping 192.168.0.1 -c 1"

subp = "sudo pkill -9 -f ADXL345_Sampler_100Hz.py"

fps_lst=[15,24]

iso_lst=[100,300]

def on():
	GPIO.output(light, 1)

def off():
	GPIO.output(light, 0)

def picture(fr,iso):
        camera.resolution = (2592, 1944)
        camera.framerate = fr
        camera.start_preview()
	pictime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-4] 
	#picTime = time.ctime()
	#t = str(picTime)
	time.sleep(5)
	camera.shutter_speed = 4000
	camera.iso = iso
        time.sleep(2)
	camera.capture('/home/pi/Documents/minion_pics/%s_FR%s_ISO%s.jpg' %(pictime,fr,iso))
	time.sleep(5)
	camera.stop_preview()

if __name__ == '__main__':

#        status = os.system(ping_hub)

#        if status == 0:
#               status = "Connected"
#		os.system(subp)
#		quit()
#        else:
#                status = "Not Connected"

#	print(status)

   	camera = PiCamera()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(light, GPIO.OUT)
#	GPIO.setup(wifi, GPIO.OUT)
#	GPIO.output(wifi, 1)

	on()
	for i in fps_lst:
    		for j in iso_lst:  
			picture(i,j)
	#picture()
	time.sleep(1)

	off()
	#time.sleep(5)
	print(pictime)

#	if status == "Connected":
#		os.system(subp)
#	else:
#		GPIO.output(wifi, 0)
#		time.sleep(6)
	print("Shutting down.")
#	time.sleep(1)
#		os.system('sudo shutdown now')
#	os.system('sudo shutdown now')
