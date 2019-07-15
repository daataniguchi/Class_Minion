import time
import RPi.GPIO as GPIO 
from picamera import PiCamera 
import os 
from subprocess import check_output 
from datetime import datetime 

GPIO.setwarnings(False)

i = 0
light = 12
#wifi = 7

ping_hub = "ping 192.168.0.1 -c 1"

subp = "sudo pkill -9 -f ADXL345_Sampler_100Hz.py"

fps_lst=[25, 30]
iso_lst=[500, 600, 700, 800]     

##Camera Functions

def off():
    GPIO.output(light, 0)  ##Light off

def on():
    GPIO.output(light, 1)  ##Light on

def picture(fr,iso,num_pic):
    camera.resolution = (2592, 1944) #Resolution for RPI
    camera.framerate = fr ##Defines framerate
    camera.iso = iso ##Defines ISO
    pictime = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-4] ##Format for naming images
    camera.shutter_speed = 4000 ##setting the shutterspeed
    for i in range(num_pic):  ##taking number of pictures determined by num_pic
        time.sleep(1) ##post adjusting shutterspeed, time in secs. sleep before capturing photo
        camera.capture('/home/pi/Documents/Test_Camera/Test_Pics/%s_FR%s_ISO%s.jpg' %(pictime,fr,iso)) ##Images captured will be stored in this path


if __name__ == '__main__':

#        status = os.system(ping_hub)

#        if status == 0:
#                status = "Connected"
        #os.system(subp)
        #quit()
#        else:
#                status = "Not Connected"

    #print(status)

    camera = PiCamera()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(light, GPIO.OUT)
    #GPIO.setup(wifi, GPIO.OUT)
    #GPIO.output(wifi, 1)

    on() ##Calling on() function
    #time.sleep(2)
    for i in fps_lst:
        for j in iso_lst:  
            picture(i,j,5) ##Calling picture() function to cycle through all FR and ISO

    off() ##Calling off() function
    #time.sleep(5)
    #print(pictime)

    #if status == "Connected":
        #os.system(subp)
    #else:
        #GPIO.output(wifi, 0)
        #time.sleep(6)
    #print("Shutting down.")
    time.sleep(1) ##Sec(s). of sleep before turning off
        os.system('sudo shutdown now') ##Shut down computer following excecusion of program
