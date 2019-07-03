##This is the code used at SIO to test camera with plankton in seawater. It was turning the monitor off as soon as the code began, so there was no way to know when it was finished. Every difference between this code and the most up to date code has been commented on. (SB)

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

fps_lst=[15,24] ##rpi_integrated code has "fps_lst=[15, 20, 25, 30]"

iso_lst=[100,300] ##rpi_integrated code has "iso_lst=[500, 600, 700, 800]"

def on():
	GPIO.output(light, 1) ##rpi_integrated code has def on() and def off() in switched positions. I don't think this would have an affect on turning the preview off though (SB)

def off():
	GPIO.output(light, 0)

def picture(fr,iso):
        camera.resolution = (2592, 1944)
        camera.framerate = fr
        camera.start_preview()
	pictime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-4] 
	#picTime = time.ctime()
	#t = str(picTime)
	time.sleep(5) ##rpi_integrated code has time.sleep(2)
	camera.shutter_speed = 4000
	camera.iso = iso ##rpi_integrated code has this after "camera.framerate = fr" 
        time.sleep(2)
	camera.capture('/home/pi/Documents/minion_pics/%s_FR%s_ISO%s.jpg' %(pictime,fr,iso))##rpi_integrated code has "camera.capture('/home/pi/Documents/Test_Camera/Test_Pics/%s_FR%s_ISO%s.jpg' %(pictime,fr,iso))"
	time.sleep(5) ##rpi_integrated code has time.sleep(2)
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
			picture(i,j)##rpi_integrated code has this repeated for a total of 5 pictures
	#picture()   ##rpi_integrated code does not have this line or the time.sleep(1) one line below
	time.sleep(1)

	off()
	#time.sleep(5)
	print(pictime) ##rpi_integrated code has this commented out

#	if status == "Connected":
#		os.system(subp)
#	else:
#		GPIO.output(wifi, 0)
#		time.sleep(6)
	print("Shutting down.") ##rpi_integrated code has this commented out
#	time.sleep(1)
#		os.system('sudo shutdown now')
#	os.system('sudo shutdown now')
