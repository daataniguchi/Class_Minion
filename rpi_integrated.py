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



##Looping through frame rate:
fps_top=30
fps_bottom=15
fps_increment=15
fps_lst=[]
i= fps_bottom

for i in range (fps_bottom,fps_top+1,fps_increment):
    fps_lst.append(i)

##Looping though ISO:

iso_top=800
iso_bottom=100
iso_increment=100
iso_lst=[]
j=iso_bottom

for j in range (iso_bottom,iso_top+1,iso_increment):
    iso_lst.append(j)              

##Combinding both lists to get all possible permutations
##Total permutations saved on total_per
combo=[]
total_per=0

for a in fps_lst:              ##for a variable (a) in list 1
    for b in iso_lst:          ##for a variable (b) in list 2
        combo.append([a,b])    ##append variables a and b into list called combo
        total_per=total_per+1
        
        
##Making an array called permu_array and placing it in a list       
permu_array=np.array(combo)
permu_array=combo

##Image naming using for loop

for i in range(total_per):
    condition=permu_array[i]
    fps=condition[0]
    iso=condition[1]
    

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
#		os.system('sudo shutdown now')
#	os.system('sudo shutdown now')  ##Shut down computer following execusion of program

