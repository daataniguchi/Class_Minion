## This code is used when the camera is deployed in water, it will sudo shutdown now
## wifi is commented out for now but left in, in case needed

import time
import RPi.GPIO as GPIO #import RPi.GPIO module
from picamera import PiCamera 
import os 
from subprocess import check_output 
from datetime import datetime 

GPIO.setwarnings(False)

i = 0
light = 12
#wifi = 7

ping_hub = "ping 192.168.0.1 -c 1" #verify IP exists and can accept requests

subp = "sudo pkill -9 -f ADXL345_Sampler_100Hz.py" #subprocess

## Framerate and ISO values to be used

fps_lst=[25, 30] #framerate in frames per second
iso_lst=[500, 600, 700, 800] #how long light is let in


##Camera Functions

def off():
	GPIO.output(light, 0)  ##Light off

def on():
	GPIO.output(light, 1)  ##Light on

def picture(fr,iso,num_pic):
	camera.resolution = (2592, 1944) #Resolution for RPI
	camera.framerate = fr ##Defines framerate
	camera.iso = iso ##Defines ISO
	pictime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-4] ##Format date for naming images
	camera.shutter_speed = 4000 ##setting the shutterspeed
	for i in range(num_pic):  ##taking number of pictures determined by num_pic
		time.sleep(1) ##sleep before capturing photo
		camera.capture('/home/pi/Documents/Test_Camera/Test_Pics/%s_FR%s_ISO%s.jpg' %(pictime,fr,iso)) ##Images captured and stored in this path

if __name__ == '__main__': 

        status = os.system(ping_hub)

        if status == 0:
                status = "Connected"
        	os.system(subp)
        	quit()
        else:
                status = "Not Connected"


	camera = PiCamera() #creating an instance of the PiCamera class
	GPIO.setmode(GPIO.BOARD) #General purpose input output, for pin numbering 
	GPIO.setup(light, GPIO.OUT) #Set GPIOlight as an output
	#GPIO.setup(wifi, GPIO.OUT) #Set GPIOwifi as an output
	#GPIO.output(wifi, 1) 

	on() ##Calling on() function
	num_pic=5
        for i in fps_lst:
        	for j in iso_lst:  
            		picture(i,j,num_pic) ##Calling picture() function to cycle through all FR and ISO and take num_pic number of pictures 

	off() ##Calling off() function
	

	if status == "Connected":
        	os.system(subp)
	else:
        	#GPIO.output(wifi, 0)
        	time.sleep(1) ##Sec(s). of sleep before turning off
        	os.system('sudo shutdown now') ##Shut down computer following excecusion of program
