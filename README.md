# SmartIoTKitchen
## Hardware requirements:
1. Raspberry pi 3/zero with wifi module.
2. Picamera module (v2).
3. Infrared module.


## Software packages requirements over raspberry pi os:
1. Python 3.x
2. Python 3 pip (pip3) package.
3. AWS CLI package.
4. RPI.GPIO package.

## Software packages requirements over AWS EC2:
1. Python 3.x
2. Python 3 pip (pip3) package.
3. Opencv 3.0 or later.
4. AWS EC2 , AWS S3, AWS SES services accounts.

## Building your own haar-cascade casifier.
Followed the tutorial by *Sentex* at www.pythonprogramming.net <br />
Link : https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/

## Sequence for given scripts:
### At raspberry pi module
1. raspb_main.py
2. configure.py
### At AWS EC2 linux instance
3. main.sh 
4. EC2_main.py
5. detect.py
6. MailToUser.py
