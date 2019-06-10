import time
import RPi.GPIO as GPIO
from picamera import PiCamera
import os
from subprocess import check_output



GPIO.setwarnings(False)

i = 0
light = 12
wifi = 7

ping_hub = "ping 192.168.0.1 -c 1"

subp = "sudo pkill -9 -f ADXL345_Sampler_100Hz.py"

def off():
	GPIO.output(light, 0)

def on():
	GPIO.output(light, 1)

def picture():
        camera.resolution = (2592, 1944)
        camera.framerate = 15
        camera.start_preview()
	#picTime = time.ctime()
	#t = str(picTime)
	time.sleep(10)
	camera.capture('/home/pi/Documents/minion_pics/%s.jpg' % pictime)
	time.sleep(5)
	camera.stop_preview()

def send():
	who = check_output("who",shell=True)
	who = who.split('(')[1]
	ip = who.split(')')[0]
#	print ip
	scp = "sudo sshpass -p 'ramboat' scp /home/pi/Documents/minion_pics/%s.jpg jack@%s:/home/jack/minion_pics/" % (pictime, ip)
	os.system(scp)
#	print scp

if __name__ == '__main__':

        status = os.system(ping_hub)

        if status == 0:
                status = "Connected"
		os.system(subp)
		quit()
        else:
                status = "Not Connected"

	print status

   	camera = PiCamera()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(light, GPIO.OUT)
	GPIO.setup(wifi, GPIO.OUT)
	GPIO.output(wifi, 1)
#	on()
	pictime = time.ctime()
	pictime = pictime.replace(" ","_")
	pictime = pictime.replace(":","-")
	picture()
#	off()
	time.sleep(5)
	print pictime

#	status = os.system(ping_hub)
#
#	if status == 0:
#		status = "Connected"
#	else:
#		status = "Not Connected"
#
#	print status

	if status == "Connected":
#		send()
		os.system(subp)
#		GPIO.output(wifi, 1)
#		quit()
	else:
		GPIO.output(wifi, 0)
		time.sleep(6)
		os.system('sudo shutdown now')
