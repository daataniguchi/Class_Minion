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
wifi = 7

ping_hub = "ping 192.168.0.1 -c 1"

subp = "sudo pkill -9 -f ADXL345_Sampler_100Hz.py"


#Looping through frame rate:
fps_top=31
fps_bottom=15
fps_increment=5
fps_lst=[]
i= fps_bottom

for i in range (fps_bottom,fps_top,fps_increment):
    fps_lst.append(i)

#Looping though ISO:

iso_top=801
iso_bottom=100
iso_increment=100
iso_lst=[]

j=iso_bottom

for j in range (iso_bottom,iso_top,iso_increment):
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
image= Image.open('dino1.jpg')
for i in range(total_per):
    condition=permu_array[i]
    fps=condition[0]
    iso=condition[1]
    

#Camera Functions:

def off():                                                                                  #Camera off
    GPIO.output(light, 0)
    
def on():                                                                                   #Camera on
    GPIO.output(light, 1)

def picture(fr,iso):
    camera.resolution = (2592, 1944)                                                        #Camera resolution
    camera.framerate = fr                                                                   #fr assigned to camera.framerate in picture function
    camera.iso= iso                                                                         #iso assigned to camera.iso in picture function
    camera.start_preview()
    pictime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-4]                          #pictime assigned to time photo was taken displaying in Years_month_day_hour-minute-seconds
    time.sleep(10)
    camera.capture('/home/pi/Documents/minion_pics/%s_FR%s_ISO%s.jpg' %(pictime,fr,iso))    #Directory where photo is saved and naming format
    camera.stop_preview()

def send():
    who = check_output("who",shell=True)
    who = who.split('(')[1]
    ip = who.split(')')[0]
#   print(ip)
    scp = "sudo sshpass -p 'ramboat' scp /home/pi/Documents/minion_pics/%s.jpg jack@%s:/home/jack/minion_pics/" % (pictime, ip)
    os.system(scp) 
#   print(scp)


if __name__ == '__main__':

#        status = os.system(ping_hub)

#       if status == 0:
#                status = "Connected"
#                os.system(subp)
#                quit()
#        else:
#               status = "Not Connected"
#	print(status)

camera = PiCamera()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
#GPIO.setup(wifi, GPIO.OUT)
#GPIO.output(wifi, 1)

#   on()
for i in fps_lst:                    #loop through i in fps_lst and j in iso_lst and call the function picture.
    for j in iso_lst:		     #This will result in camera.framerate and camera.iso cycling through a different value, taking a photo and going to the next value.  
	picture(i,j)
        
   off()
#time.sleep(5)

#   status = os.system(ping_hub)
#
#   if status == 0:
#       status = "Connected"
#   else:
#       status = "Not Connected"
#
#   print(status)


#if status == "Connected":
#       send()
        os.system(subp)
#       GPIO.output(wifi, 1)
#       quit()
else:
        GPIO.output(wifi, 0)
        time.sleep(6)
        os.system('sudo shutdown now')

