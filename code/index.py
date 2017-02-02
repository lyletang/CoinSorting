# Coin sorting
# Author: Jiahui Tang

#coding:utf-8
from colorlabeler import ColorLabeler
#from shapedetector import ShapeDetector
import imutils
import cv2
import time
import os
import serial
import RPi.GPIO as GPIO

port = "/dev/ttyACM0"
serialFromArduino = serial.Serial(port,9600)

light = 12
led = 5
war = 4

reply_up = 23
reply_down = 24
reply_rec = 25

reply_one = 6
reply_five = 21
reply_ten = 20

reply_t1 = 13
reply_t5 = 19
reply_t10 = 26

moneyNumber = 0
oneFlag = 0
fiveFlag = 0
tenFlag = 0
falFlag = 0
moneyType = 0

while 1:
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(light,GPIO.IN)
    GPIO.setup(led,GPIO.OUT)
    GPIO.setup(war,GPIO.OUT)
    GPIO.output(led,False)
    GPIO.setup(reply_up,GPIO.OUT)
    GPIO.setup(reply_down,GPIO.OUT)
    GPIO.setup(reply_rec,GPIO.OUT)

    GPIO.setup(reply_one,GPIO.OUT)
    GPIO.setup(reply_five,GPIO.OUT)
    GPIO.setup(reply_ten,GPIO.OUT)
    GPIO.setup(reply_t1,GPIO.OUT)
    GPIO.setup(reply_t5,GPIO.OUT)
    GPIO.setup(reply_t10,GPIO.OUT)
    
    GPIO.output(war,False)
    
    GPIO.output(reply_up,False)
    GPIO.output(reply_down,False)
    GPIO.output(reply_rec,False)
    
    GPIO.output(reply_t1,False)
    GPIO.output(reply_t5,False)
    GPIO.output(reply_t10,False)
     
    GPIO.output(reply_one,False)
    GPIO.output(reply_five,False)
    GPIO.output(reply_ten,False)

    if(GPIO.input(light)==1):
        GPIO.output(reply_up,True)
        time.sleep(0.5)
        GPIO.output(reply_up,False)
        time.sleep(0.5)
    if(GPIO.input(light)==0):
        text = " "
        truearea = 0
        #time.sleep(1)
        GPIO.output(reply_up,True) 
        time.sleep(0.3)
        GPIO.output(reply_up,False)
        GPIO.output(reply_down,True)
        GPIO.output(reply_up,True) 
        time.sleep(0.3)
        GPIO.output(reply_up,False)
        time.sleep(0.2)
        GPIO.output(reply_down,False)
        #time.sleep(1)
        GPIO.output(led,True)

        capture = cv2.VideoCapture(0)
        ret,img = capture.read()
        cv2.imwrite("/home/pi/2016/1.png",img)
        image = cv2.imread("/home/pi/2016/1.png")
        #os.remove("/home/pi/2016/1.png")
        resized = imutils.resize(image)
        #ratio = image.shape[0] / float(resized.shape[0])
        # convert the resized image to grayscale, blur it slightly,
        # and threshold it
        blurred = cv2.GaussianBlur(resized, (5,5),0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        #corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
        #print len(corners)
        #blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
        thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
        # find contours in the thresholded image and initialize the
        # shape detector
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        cl = ColorLabeler()
        # loop over the contours
        for c in cnts:
            #hull = cv2.isContourConvex(c)
            area = cv2.contourArea(c)
            #print "area:",area
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            #cX = int((M["m10"] / M["m00"])*ratio)
            #cY = int((M["m01"] / M["m00"])*ratio)
            #shape = sd.detect(c)
            color = cl.label(lab,c)
            #print "color:",color
            #text = "{}".format(color)
            #corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
            #length = len(corners)
            c = c.astype("float") 
            #c *= ratio
            c = c.astype("int")
            #cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            #cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1)
            # show the output image
            #cv2.imshow("Image", image)
            if area > 20000:
                truearea = area
        GPIO.output(led,False)
        if truearea>107000:
            moneyNumber = moneyNumber + 1
            tenFlag = 1
            text = "one yuan"
            GPIO.output(reply_rec,True)
            GPIO.output(reply_up,True) 
            time.sleep(0.3)
            GPIO.output(reply_up,False)
            time.sleep(0.2)
            GPIO.output(reply_rec,False)
            #time.sleep(1)
            
            GPIO.output(reply_t1,True)
            GPIO.output(reply_one,True)
            GPIO.output(reply_t5,True)
            GPIO.output(reply_five,True)
            GPIO.output(reply_t10,True)
            time.sleep(0.5)
            GPIO.output(reply_t1,False)
            GPIO.output(reply_one,False)
            GPIO.output(reply_t5,False)
            GPIO.output(reply_five,False)
            GPIO.output(reply_t10,False)
            serialFromArduino.write('3')
        elif truearea>88000:
            GPIO.output(war,True)
            text = "FALSE RMB"
            falFlag = 1
            moneyNumber = moneyNumber + 1

            GPIO.output(reply_rec,True)
            GPIO.output(reply_up,True) 
            time.sleep(0.3)
            GPIO.output(reply_up,False)
            time.sleep(0.2)
            GPIO.output(reply_rec,False)
            #time.sleep(1)
            GPIO.output(reply_t1,True)
            GPIO.output(reply_one,True)
            GPIO.output(reply_t5,True)
            GPIO.output(reply_five,True)
            GPIO.output(reply_t10,True)
            GPIO.output(reply_ten,True)
            time.sleep(0.6)
            GPIO.output(reply_t1,False)
            GPIO.output(reply_one,False)
            GPIO.output(reply_t5,False)
            GPIO.output(reply_five,False)
            GPIO.output(reply_t10,False)
            GPIO.output(reply_ten,False)
            GPIO.output(war,False)
            serialFromArduino.write('4')
        elif truearea > 74000:
            text = "five jiao"
            fiveFlag = 1
            moneyNumber = moneyNumber + 1
            
            GPIO.output(reply_rec,True)
            GPIO.output(reply_up,True) 
            time.sleep(0.3)
            GPIO.output(reply_up,False)
            time.sleep(0.2)
            GPIO.output(reply_rec,False)
            
            
            GPIO.output(reply_t1,True)
            GPIO.output(reply_one,True)
            GPIO.output(reply_t5,True)
            time.sleep(0.35)            
            GPIO.output(reply_t1,False)
            GPIO.output(reply_one,False)
            GPIO.output(reply_t5,False)
            serialFromArduino.write('2')
        elif truearea > 50000 :
            text = "one jiao"
            oneFlag = 1
            moneyNumber = moneyNumber + 1
            
            GPIO.output(reply_rec,True)
            GPIO.output(reply_up,True)
            
            time.sleep(0.2)
            GPIO.output(reply_up,False)
            time.sleep(0.2)
            GPIO.output(reply_rec,False)
            
            GPIO.output(reply_t1,True)
            time.sleep(0.4)
            GPIO.output(reply_t1,False)
            serialFromArduino.write('1')
        else:
            pass
        if oneFlag and fiveFlag and tenFlag and falFlag:
            moneyType = 4
        elif oneFlag and fiveFlag and tenFlag:
            moneyType = 3
        elif oneFlag and fiveFlag and falFlag:
            moneyType = 3
        elif oneFlag and tenFlag and falFlag:
            moneyType = 3
        elif fiveFlag and tenFlag and falFlag:
            moneyType = 3
        elif oneFlag and fiveFlag :
            moneyType = 2
        elif oneFlag and tenFlag :
            moneyType = 2
        elif oneFlag and falFlag :
            moneyType = 2
        elif fiveFlag and tenFlag :
            moneyType = 2
        elif fiveFlag and falFlag :
            moneyType = 2
        elif tenFlag and falFlag :
            moneyType = 2
        elif oneFlag :
            moneyType = 1
        elif fiveFlag :
            moneyType = 1
        elif tenFlag :
            moneyType = 1
        elif falFlag :
            moneyType = 1
        else:
            pass
        print "area:",truearea,"money:",text,"number:",moneyNumber,"Type:",moneyType
        #print "money:",text
        #cv2.putText(image, text, (100, 100), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1)
        #k = cv2.waitKey(0) & 0xff
        #k = cv2.waitKey(0) & 0xff
        #if k == 27:
        #    break
        #else :
        #    pass
        GPIO.cleanup()
        capture.release()
GPIO.cleanup()
capture.release()
#cv2.destroyAllWindows()
