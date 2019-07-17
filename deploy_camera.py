## This code is used when the camera is deployed in water, it will sudo shutdown now
## wifi is commented out for now but left in, in case needed

## Importing libraries

import time 
import RPi.GPIO as GPIO 
from picamera import PiCamera 
import os 
from subprocess import check_output 
from datetime import datetime 

##Setting up the system

GPIO.setwarnings(False) ##disables warning messages 

light = 12 ##Light is set to be pin 12  
#wifi = 7 ##wifi is set to be pin 7

ping_hub = "ping 192.168.0.1 -c 1" ##verify IP exists and can accept requests

subp = "sudo pkill -9 -f ADXL345_Sampler_100Hz.py" ##stops the code ADXL345_Sampler_100Hz.py

## Framerate and ISO values to be used

fps_lst=[25, 30] ##framerate in frames per second
iso_lst=[800] ##how long light is let in


## Camera Functions

def off():
	GPIO.output(light, 0)  ##Light off

def on():
	GPIO.output(light, 1)  ##Light on

def picture(fr,iso,num_pic):
	camera.resolution = (2592, 1944) ##Resolution for Raspberry Pi
	camera.framerate = fr ##Defines framerate
	camera.iso = iso ##Defines ISO
	pictime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-4] ##Format date for naming images
	camera.shutter_speed = 4000 ##setting the shutterspeed
	for k in range(num_pic):  ##taking number of pictures determined by num_pic
		time.sleep(1) ##sleep before capturing photo
		camera.capture('/home/pi/Documents/Test_Camera/Test_Pics/%s_FR%s_ISO%s.jpg' %(pictime,fr,iso)) ##Images captured and stored in this path


if __name__ == '__main__': #if this is the main code then executes following code 

        status = os.system(ping_hub) #checks connection to os 


        if status == 0: # means connection is good, runs stop code 'subp' then quits
                status = "Connected"
        	os.system(subp)
        	quit()
        else:
                status = "Not Connected" # if ping returns a non-zero value the connection failed


	camera = PiCamera() #creating an instance of the PiCamera class
	GPIO.setmode(GPIO.BOARD) #General purpose input output, for pin numbering 
	GPIO.setup(light, GPIO.OUT) #Set light as an output
	#GPIO.setup(wifi, GPIO.OUT) #Set wifi as an output
	#GPIO.output(wifi, 1) #turns wifi on

	on() ##Calling on() function
	num_pic=5 #defines how many pictures to take at a particular camera setting
        for i in fps_lst:
        	for j in iso_lst:  
            		picture(i,j,num_pic) ##Calling picture() function to cycle through all FR and ISO and take num_pic number of pictures 

	off() ##Calling off() function
	

	if status == "Connected": #if connected run 
        	os.system(subp) #kills 'subp'
	else:
        	#GPIO.output(wifi, 0) # turns wifi off
        	time.sleep(1) ##sleep before turning off
        	os.system('sudo shutdown now') ##Shut down computer following execusion of program
