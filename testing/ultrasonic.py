# -*- coding: utf-8 -*-
"""
Created on Sep 25 09:05:03 2021
#reference https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
@author: pcochang
"""
import RPI.GPIO as GPIO 
import time
GPIO.setmode(GPIO.BCM)

def GPIO_init():
    global TRIG
    TRIG = 23 
    global ECHO
    ECHO = 24
    GPIO.setup (TRIG, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.setup (ECHO, GPIO.IN)
    
    
def measureDistance_cm():
    GPIO.output (TRIG, True) 
    time.sleep(0.00001) 
    GPIO.output (TRIG, False)
    
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round (distance, 2)    
    return distance
