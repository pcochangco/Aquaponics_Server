# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 15:06:28 2021

@author: pcochang
"""

import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def GPIO_init():
    global Motor1
    Motor1 = {'EN': 19, 'input1': 21, 'input2': 22}
    for x in Motor1:
        GPIO.setup(Motor1[x], GPIO.OUT)
    global EN1
    EN1 = GPIO.PWM(Motor1['EN'], 100)    
    EN1.start(0)  

def runMotor():
    print ("Motor running")
    if True:
        EN1.ChangeDutyCycle(50) #50% dutycycle
        GPIO.output(Motor1['input1'], GPIO.HIGH)
        GPIO.output(Motor1['input2'], GPIO.LOW)
        sleep(3)
        #if some conditions here:
            #break
    print ("STOP")
    EN1.ChangeDutyCycle(0)
    
GPIO_init()
runMotor()
