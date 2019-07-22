#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from picamera import PiCamera
import os
from subprocess import check_output

GPIO.setwarnings(False)

i = 0
light = 12
wifi = 38

net_cfg = "ls /etc/ | grep dhcp"

ping_hub = "ping 192.168.0.1 -c 1"

ping_google = "ping google.com -c 1"

iwlist = 'sudo iwlist wlan0 scan | grep "Class_Hub"'

subp = "sudo pkill -9 -f ADXL345_Sampler_100Hz.py"

fps_lst=[25, 30] ##framerate in frames per second
iso_lst=[500,600,700,800] ##how long light is let in
num_pic=5 #defines how many pictures to take at a particular camera setting


def flash():
    j = 0
    while j <= 2:
        GPIO.output(light, 1)
        time.sleep(.25)
        GPIO.output(light, 0)
        time.sleep(.25)
        j = j + 1

def off():
    GPIO.output(light, 0)

def on():
    GPIO.output(light, 1)

def picture(fr,iso):
    camera.resolution = (2592, 1944) ##Resolution for Raspberry Pi
    camera.framerate = fr ##Defines framerate
    camera.iso = iso ##Defines ISO
    pictime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-4] ##Format date for naming images
    camera.shutter_speed = 4000 ##setting the shutterspeed
    camera.start_preview()
    camera.capture('/home/pi/Documents/minion_pics/minpic_%s_FR%s_ISO%s.jpg' %(pictime,fr,iso)) #this format for capturing and saving pictures at SIO
    camera.stop_preview()
       

if __name__ == '__main__':
    camera = PiCamera()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(light, GPIO.OUT)
    GPIO.setup(wifi, GPIO.OUT)
    GPIO.output(wifi, 0)

    on()

    for k in range(num_pic):
        for i in fps_lst:
            for j in iso_lst:
                time.sleep(2) ##sleep before capturing photo
                picture(i,j,num_pic) ##Calling picture() function to cycle through all FR and ISO and take num_pic number of pictures 

    off() ##Calling off() function

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
        flash()
        quit()
    else:
        GPIO.output(wifi, 1)
        time.sleep(5)
        os.system('sudo shutdown now')
