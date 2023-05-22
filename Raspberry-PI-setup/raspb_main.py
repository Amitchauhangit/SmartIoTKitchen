import RPi.GPIO as GPIO
import time
import picamera # should install picamera : sudo apt-get install python-picamera
import random
from storageUtil import uploadBlob

camera = picamera.PiCamera() #camera object
filepath = "input-image-" + random.randint(1, 10000) + ".jpg"
camera.capture()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor

i=0
while i!=1:
    print("checking")
    
    i=GPIO.input(11)

if i==1:               #When output from motion sensor is HIGH
    
    print("enter")
	
    time.sleep(1)
	
    uploadBlob(filepath)
	
    print("done")
    
