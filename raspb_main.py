# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:00:52 2018

@author: Dragon
"""
import subprocess
import RPi.GPIO as GPIO
import time
import awsconfig
import picamera # should install picamera : sudo apt-get install python-picamera

camera = picamera.PiCamera() #camera object
camera.capture("input_image.jpg")


awsconfig.config()

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
	
    subprocess.call(["sudo","aws","s3","cp","input_image.jpg","s3://imagebox1234/image_rasp/image1.jpg"]) 
	
    subprocess.call(["plink -ssh ubuntu@ec2-52-14-127-155.us-east-2.compute.amazonaws.com -i aws_iot.ppk /home/ubuntu/main.sh",shell=True])
	#used plink command line tool for establishing ssh connection with the aws ec2 instance.
	
    print("done")
    

