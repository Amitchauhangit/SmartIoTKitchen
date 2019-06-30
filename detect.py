import numpy as np
import cv2
import glob
import os
import subprocess

def det():
    
    
    bean_cascade2 = cv2.CascadeClassifier('beancascade.xml')
    
    
    template=cv2.imread('test7.jpg',0)
    width,height=template.shape[::-1]
    
    thresold=0.65
    
    pic=1
    r=10
    t=12
    path="images/"
    output_file="combined_result/"
    crop_path="cropped_result/"
    
    seq=0
    
    for filename in glob.glob(os.path.join(path, '*.jpg')) :
            
                try:
                    seq+=1
                
                    img=cv2.imread(filename)
                    img2=cv2.imread(filename)
                    img_gray= cv2.imread(filename,0)
                    
                                  
					#Phase 1 : Finding Jar(s) top coordinates.
					
                    res=cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                    loc=np.where(res>=thresold)
 
                    modified=[]
                    for pt in zip(*loc[::-1]):
                        modified.append(pt)
						
                    modified.sort()
                    modified.append((-1,-1))
                    
                    mod=[]
    
                    for i in range(len(modified)):
                        if i==0:
                            
                            c=0
                            a=modified[i][0]
                            b=modified[i][1]
                            
                        elif (abs(modified[i][0]-modified[c][0])<=width and i<len(modified)-1):
                            a+=modified[i][0]
                            b+=modified[i][1]
                    
                        else:
                            a=a//(i-c)		#taking mean coordinates (a,b) for single jar.
                            b=b//(i-c)
    #                        print("i: ",i,"c: ",c)
                            mod.append((a,b)) # registering the found jar coordinates.
							
                            c=i				#changing pivot value.
                            
							#initiating from the new jar coordinates.
                            a=modified[i][0]
                            b=modified[i][1]
                            
                    print("Number of jars found:",len(mod)) #total number of jars in the picture.
                    
					
					#Phase 2 : Detecting object in the jar(s) individually and processing their object heights.
					
                    bean2 = bean_cascade2.detectMultiScale(img_gray, r,t,minSize=(100,100)) 
                    for (x,y,w,h) in bean2:
                         cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),4) #marking image with yellow rectangles.
                    
                    #building a composite rectangle to cover the whole jar cap.
                    crop_image_sequence=0
                    for jarstart,jarend in mod:
                        
                        
                        cv2.rectangle(img,(jarstart, jarend),(jarstart+width,jarend+height),(0,255,255),20) #marking rectangle over this particular jar cap.
        
                        jarcap_end=[jarstart+width,jarend+height]
        
                    
                        bean=[]      
                        
                        for k in bean2 :
                            if ((k[0]>=jarstart) and (k[0]<=jarcap_end[0]) and (k[1]>jarcap_end[1])):
                                
                                bean.append((k[1],k[0],k[2],k[3])) #entering in (y,x,h,w) manner to further sort in terms of height
        
                        bean.sort()
                        count,c,i=0,0,0
                        
						
						#getting topmost object(bean) height and removing outliers if any.
                        while True:
                            if(count==3 or i>=len(bean)-1):
                                break
                            if(abs(bean[i][0]-bean[i+1][0])<bean[i][2]): #if difference in heights of two rectangle beans is less then the height of first one.
                                    i+=1
                                    count+=1
                            else:
                                    bean.pop(i)
                                    c+=1
                                    i=c
                                    count=0
                        b=[]
                        b.append(bean[0][0])
                        average_top=0
                        
                        
                        for i in range(1,len(bean)):
                            if(abs(bean[0][0]-bean[i][0])<=(bean[0][2]//2)):
                                b.append(bean[i][0])
                            else:
                                break
                            
                        average_top=sum(b)//len(b)		#  topmost coordinates of item.
                        
						#same for bottom coordinates.
                        bottom=bean[-1][0]+bean[-1][2] # bottom = x+h.
                        cv2.rectangle(img,(jarstart,average_top),(jarcap_end[0],bottom),(0,0,255),10)
                        
                        total=abs(bottom-jarcap_end[1])		#total height of a jar.
                        item_size=abs(bottom-average_top)	#total height of item stored in jar.
                        percentage=item_size/total			#percentage of that item.
                        
                        print(total,item_size,percentage,sep="\n")
                        print(width," ",item_size)
                        
                        if (percentage<=0.4):
                            crop_image_sequence+=1
                            
                            
                            crop_img = img2[average_top-40:bottom, jarstart:jarcap_end[0]]
                            print("image capture")
                            resized_image = cv2.resize(crop_img,(400,200))
							
                            
                        result_cropped_image = crop_path+str(seq)+"-"+str(crop_image_sequence)+".jpg"
                        cv2.imwrite(result_cropped_image , resized_image)
							
							 #to store same in s3 bucket.
                        subprocess.call(["aws","s3","cp",result_cropped_image,"s3://imagebox1234/image_to_show/image"+str(seq)+".jpg"]) 
							
                        
                    print("writing image ",seq)
                    cv2.imwrite(output_file+str(seq)+".jpg",img)
                    print()
                    
                    
                    
                    
                    pic+=1
                except Exception as e:
                    print(e)
                    pic+=1

