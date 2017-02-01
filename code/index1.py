# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
#import serial

reply_one = 6
reply_five = 21
reply_ten = 20

reply_t1 = 13
reply_t5 = 19
reply_t10 = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(reply_one,GPIO.OUT)
GPIO.setup(reply_five,GPIO.OUT)
GPIO.setup(reply_ten,GPIO.OUT)
GPIO.setup(reply_t1,GPIO.OUT)
GPIO.setup(reply_t5,GPIO.OUT)
GPIO.setup(reply_t10,GPIO.OUT)
GPIO.output(reply_t1,True)
GPIO.output(reply_t5,True)
GPIO.output(reply_t10,True)
     
GPIO.output(reply_one,True)
GPIO.output(reply_five,True)
GPIO.output(reply_ten,True)
#PIO.output(reply_t1,True)

#port = "/dev/ttyACM0"
#serialFromArduino = serial.Serial(port,9600)
#serialFromArduino.write('2')
while 1 :        
    #GPIO.output(reply_ten,False)
    #GPIO.output(reply_t1,False)
    #GPIO.output(reply_one,False)            
    #GPIO.output(reply_t5,False)
    GPIO.output(reply_five,False)
    #GPIO.output(reply_t10,False)
    time.sleep(2)
    #GPIO.output(reply_t1,True)
    #GPIO.output(reply_one,True)
    #GPIO.output(reply_t5,True)
    GPIO.output(reply_five,True)
    #GPIO.output(reply_t10,True)
    #GPIO.output(reply_ten,True)
    time.sleep(2)
