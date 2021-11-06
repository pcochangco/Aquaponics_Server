# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 15:06:28 2021

@author: pcochang
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 15:55:43 2021

@author: pcochang
"""

#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

in1 = 11
in2 = 12
in3 = 13
in4 = 15
 
motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0

GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002
step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°
direction = False # True for clockwise, False for counter-clockwise
# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
 
def cleanup():
    GPIO.output( in1, 0 )
    GPIO.output( in2, 0 )
    GPIO.output( in3, 0 )
    GPIO.output( in4, 0 )
 
 
cleanup()
try:
    i = 0
    for i in range(step_count):
        for x, pin in enumerate(motor_pins):
            GPIO.output( pin, step_sequence[motor_step_counter][x] )
        if direction==True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif direction==False:
            motor_step_counter = (motor_step_counter + 1) % 8
        time.sleep( step_sleep )
 
except KeyboardInterrupt:
    cleanup()
 
cleanup()

