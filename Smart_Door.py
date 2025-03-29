import numpy as np
import cv2
import imutils
import time
import os
#import email packages
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


print ("All packages imported properly!")


def mask_image(img):
    mask=np.zeros((img.shape[0], img.shape[1]),dtype="uint8")

    # for i in range(0,4):
    #   bbox=cv2.selectROI(img, False)
    #   print(bbox)
    pts= np.array([ [850,50],[1125,50],[1125,700],[650,711]])
    cv2.fillConvexPoly(mask,pts,255)

    masked=cv2.bitwise_and(img,img,mask=mask)
    gray= imutils.resize(masked,width=200)
    gray=cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
    gray= cv2.GaussianBlur(gray,(11,11),0)

    return masked, gray

counter=0

while True:
    counter=counter+1
    print()
    print("---Times through loop since starting: "+str(counter)+"---")
    print()

    command = 'libcamera-still -t 2100 --timelapse 1000 --width 1280 --height 720 --vflip --hflip -o test%02d.jpg'
    os.system(command)
    time.sleep(1)
    
    
    print("Captured 1st and 2nd image")

    test1 = cv2.imread("test00.jpg") 
    test2 = cv2.imread("test01.jpg")
    masked1, gray1 = mask_image(test1)
    masked2, gray2 = mask_image(test2)  

    

    #Compare the two images

    pixel_thres =50
    detector_total=np.uint64(0)
    detector=np.zeros((gray2.shape[0],gray2.shape[1]), dtype="uint8")

    #pixel by pixel comparison

    for i in range(0, gray2.shape[0]):
        for j in range(0,gray2.shape[1]):
            if abs(int(gray2[i,j])-int(gray1[i,j]))> pixel_thres:
                detector[i,j]=255

    #Sum detector array
    detector_total=np.uint64(np.sum(detector))
    print("detector total= "+str(detector_total))

    #time.sleep(2)

    if detector_total>4000:
        print("Someone is at the door")
        #Define a unique video file
        timestr = time.strftime("doorbell-%Y%m%d-%H%M%S")
        command2 = (
            f'libcamera-vid -t 5000 '
            f'--width 1280 --height 720 '
            f'--framerate 30 '
            f'--vflip --hflip '
            f'-o {timestr}.h264'
        )
        os.system(command2)

        print("Finished recording, converting to mp4")
        command3 = f'ffmpeg -y -framerate 30 -i {timestr}.h264 -c copy {timestr}.mp4'
        os.system(command3)

        print("Finished converting file")

        #Write images to files
        cv2.imwrite("gray1.jpg", gray1)
        cv2.imwrite("gray2.jpg", gray2)
        cv2.imwrite("masked1.jpg", masked1)
        cv2.imwrite("masked2.jpg", masked2)
        
        # ------------------------------------Email photos to user----------------------------------------------
        smtpUser= "email@gmail.com"
        smtpPass="password"

        #Destination
        toAdd= "sendemail@gmai.com"
        fromAdd=smtpUser
        f_time=datetime.now().strftime("%a %d %b @ %H:%M")
        subject="Smart Doorbell Photos from: "+f_time
        msg= MIMEMultipart()
        msg["Subject"]=subject
        msg["From"]=fromAdd
        msg["To"]=toAdd

        msg.preamble="Smart Doorbell Photos from: "+f_time

        #Email Text
        body= MIMEText("Smart Doorbell Photos from: "+f_time)
        msg.attach(body)

        #Attach images test0,test1, gray0,gray1,masked0,masked1
        fp= open('test00.jpg', 'rb')
        img=MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        fp= open('test01.jpg', 'rb')
        img=MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        fp= open('gray1.jpg', 'rb')
        img=MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        fp= open('gray2.jpg', 'rb')
        img=MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        fp= open('masked1.jpg', 'rb')
        img=MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        fp= open('masked2.jpg', 'rb')
        img=MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        #Send Email

        s= smtplib.SMTP("smtp.gmail.com",587)

        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(smtpUser,smtpPass)
        s.sendmail(fromAdd,toAdd, msg.as_string())
        s.quit()

        print("Email Delivered...")

        
    else:
        print("Nothing detected")
#Read in image
# test1 = cv2.imread("tD.jpg")
# gray1=mask_image(test1)
# cv2.imshow("Original", test1)

# cv2.imshow("Masked", gray1)