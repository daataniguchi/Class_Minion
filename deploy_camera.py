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

fps_lst=[15, 20, 25, 30]
iso_lst=[100, 200, 300, 400, 500, 600, 700, 800]    

##Camera Functions

def off():
	GPIO.output(light, 0)  ##General purpose input output. Output pins turn RPI on or off.
			       ##Light off

def on():
	GPIO.output(light, 1)  ##Light on

def picture(fr,iso):
        camera.resolution = (2592, 1944) #Resolution for RPI
        camera.framerate = fr ##Cycling through framerate
	camera.iso = iso ##Cycling through ISO
        camera.start_preview() ##Displays what is currently in camera frame
	pictime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-4] ##Format for naming images
	#picTime = time.ctime()
	#t = str(picTime)
	time.sleep(7) ##upon start preview, time in seconds of sleep before adjusting shutter speed    
	camera.shutter_speed = 4000
        time.sleep(3) ##post adjusting shutterspeed, time in secs. sleep before capturing photo
	camera.capture('/home/pi/Documents/Test_Camera/Test_Pics/%s_FR%s_ISO%s.jpg' %(pictime,fr,iso)) ##Images captured will be stored in this path
	time.sleep(2) ## seconds of sleep after photo is captured before stop preview
	camera.stop_preview() ##Display showing what is in camera frame closes.
			      ##This programs will loop until all photos are taken.

if __name__ == '__main__':

#        status = os.system(ping_hub)

#        if status == 0:
#                status = "Connected"
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

	on() ##Calling on() function
#	time.sleep(2)
	for i in fps_lst:
    		for j in iso_lst:  
			picture(i,j) ##Calling picture() function to cycle through all FR and ISO

	off() ##Caling off() function
	#time.sleep(5)
	#print(pictime)

#	if status == "Connected":
#		os.system(subp)
#	else:
#		GPIO.output(wifi, 0)
#		time.sleep(6)
	#print("Shutting down.")
	time.sleep(1) ##Sec(s). of sleep before turning off
		os.system('sudo shutdown now') ##Shut down computer following excecusion of program
	os.system('sudo shutdown now')  ##Shut down computer following execusion of program

