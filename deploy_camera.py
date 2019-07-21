#!/usr/bin/env python

## Importing libraries

import time
import RPi.GPIO as GPIO
from picamera import PiCamera
import os
from subprocess import check_output
from datetime import datetime

## Setting up the system

GPIO.setwarnings(False) #disables warning messages

i = 0
light = 12 #light is set to be pin 12
wifi = 38 #wifi is set to be pin 38

net_cfg = "ls /etc/ | grep dhcp" #configures network

ping_hub = "ping 192.168.0.1 -c 1" #verify IP exists and can accept requests

ping_google = "ping google.com -c 1" #test reachability of a host on the IP network

iwlist = 'sudo iwlist wlan0 scan | grep "Class_Hub"' #scan for available wireless networks and display additional information about them

subp = "sudo pkill -9 -f ADXL345_Sampler_100Hz.py" #stops the code ADXL345_Sampler_100Hz.py

## Framerate and iso values to be used

fps_lst = [25, 30] #framerate in frames per second
iso_lst = [500, 600, 700, 800] #how long light is let in 

## Camera Functions

def flash(): #I don't know what this does, maybe makes the LED flash 
	j = 0
	while j <= 2:
		GPIO.output(light, 1)
		time.sleep(.25)
		GPIO.output(light, 0)
		time.sleep(.25)
		j = j + 1

def off():
    GPIO.output(light, 0) #light off 

def on():
	GPIO.output(light, 1) #light off

def picture(fr,iso):
    #pictime = time.asctime(time.gmtime())
    pictime = os.popen("sudo hwclock -r").read() #format for real time clock 
    pictime = pictime.split('.',1)[0]
    pictime = pictime.replace("  ","_") #replaces a space with an underscore
    pictime = pictime.replace(" ","_") #replaces a space with an underscore
    pictime = pictime.replace(":","-") #replaces a colon with a hyphen
    pictime = pictime.split('.',1)[0]
    pictime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-4] #format date for naming images
    on() #calling on function
    camera.resolution = (2592, 1944) #resolution for Raspberry Pi
    camera.framerate = fr #defines framerate
    camera.iso = iso #defines iso
    camera.shutter_speed = 4000 # setting the shutter speed
    camera.start_preview() #when connected to a monitor this turns on camera preview
    time.sleep(10) #ten second sleep
	#camera.capture('/home/pi/Documents/minion_pics/minpic_%s_FR%s_ISO%s.jpg' %(pictime,fr,iso)) #this format for capturing and saving pictures at SIO
    camera.capture('/home/pi/Documents/Test_Camera/Test_Pics/%s_FR%s_ISO%s.jpg' %(pictime,fr,iso)) #this format for capturing and saving Images at CSUSM
    time.sleep(5) #five second sleep
    camera.stop_preview() #when connected to a monitor this turns off camera preview 
    time.sleep(.5) # half second sleep
    off() #calling off function

if __name__ == '__main__': #if this is the main code then executes following code 
    camera = PiCamera() #creating an instance of the PiCamera class
    GPIO.setmode(GPIO.BOARD) #General purpose input output, for pin numbering
    GPIO.setup(light, GPIO.OUT) #sets light as an output
    GPIO.setup(wifi, GPIO.OUT) #sets wifi as an output
    GPIO.output(wifi, 0) #turns wifi on
    num_pic = 5 #defines how many pictures to take at a particular camera setting
    for k in range(num_pic):
        for x in fps_lst:
            for y in iso_lst:
                time.sleep(2)
                picture(x,y) #Calling picture() function to cycle through all FR and ISO and take num_pic number of pictures
    #print(pictime)

    wifi_status = os.popen(iwlist).read()

    if "Class_Hub" in wifi_status:
        print("WIFI!!")
        status = "Connected"
        net_status = os.popen(net_cfg).read()
        if ".minion" in net_status:
            os.system("ifswitch")
        else:
            print("You have Minions!")

    else:
        print("No wifi...")
        status = "Not Connected"

    if status == "Connected":
        os.system(subp)
        GPIO.output(wifi, 0)
        flash() #calls flash function 
        quit()
    else:
        GPIO.output(wifi, 1)
        time.sleep(5)
        os.system('sudo shutdown now')