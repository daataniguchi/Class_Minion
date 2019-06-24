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



#Looping through frame rate:
fps_top=30
fps_bottom=15
fps_increment=10
fps_lst=[]
i= fps_bottom

for i in range (fps_bottom,fps_top+1,fps_increment):
    fps_lst.append(i)

#Looping though ISO:

iso_top=800
iso_bottom=100
iso_increment=200
iso_lst=[]
j=iso_bottom

for j in range (iso_bottom,iso_top+1,iso_increment):
    iso_lst.append(j)              

#Combinding both lists to get all possible permutations
#Total permutations saved on total_per
combo=[]
total_per=0

for a in fps_lst:              #for a variable (a) in list 1
    for b in iso_lst:          #for a variable (b) in list 2
        combo.append([a,b])    #append variables a and b into list called combo
        total_per=total_per+1
        
        
#Making an array called permu_array and placing it in a list       
permu_array=np.array(combo)
permu_array=combo

#Image naming using for loop

for i in range(total_per):
    condition=permu_array[i]
    fps=condition[0]
    iso=condition[1]
    

def off():
	GPIO.output(light, 0)

def on():
	GPIO.output(light, 1)

def picture(fr,iso):
        camera.resolution = (2592, 1944)
        camera.framerate = fr
	camera.iso = iso
        camera.start_preview()
	pictime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-4] 
	#picTime = time.ctime()
	#t = str(picTime)
	time.sleep(2) #why for do you sleep here changed from 5 to 2
	camera.shutter_speed = 4000
        time.sleep(2) #common practice to sleep before taking a picture
	camera.capture('/home/pi/Documents/minion_pics/%s_FR%s_ISO%s.jpg' %(pictime,fr,iso))
	time.sleep(2) 
	camera.stop_preview()

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

	on()
#	time.sleep(2)
	for i in fps_lst:
    		for j in iso_lst:  
			picture(i,j)
	#picture()
	

	off()
	#time.sleep(5)
	#print(pictime)

#	if status == "Connected":
#		os.system(subp)
#	else:
#		GPIO.output(wifi, 0)
#		time.sleep(6)
	#print("Shutting down.")
	time.sleep(1)
#		os.system('sudo shutdown now')
	os.system('sudo shutdown now')
