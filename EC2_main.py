import subprocess
import time
import detect

subprocess.call(["aws","s3","cp","s3://imagebox1234/image_rasp/recent_image.jpg","images/input_image.jpg"]) 
print("image_downloaded")
time.sleep(1)

detect.det()




print("end")