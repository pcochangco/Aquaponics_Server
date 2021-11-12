# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 19:25:16 2021

@author: pcochang
"""

import numpy as np
import cv2
import math
import os, shutil
import time
import timeit
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

start_with_motor = timeit.default_timer()

def delete_img(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except:
            folder = "/home/pi/Pictures0_" + str(time.time()) +"/"
            break
    return folder

def takeImage(directory):
    from picamera import PiCamera
    camera = PiCamera()
    time.sleep(2)
    camera.resolution = (1280, 720)
    camera.vflip = True
    camera.contrast = 10
    file_name = os.path.join(directory,"img_" + str(time.time()) + ".jpg")
    camera.capture(file_name)
    print("Picture taken.")
    
    
def ratio_to_actual(image_pixel_ratio):
    return image_pixel_ratio * 1

def get_lettuce_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([30, 50, 50])
    upper = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    return mask

#get center of contoured image
def center(contours, image):
    image_y, image_x, _ = image.shape
    cnts = [x for x in contours if cv2.contourArea(x) > image_x*image_y*0.01]
    distance = []
    for c in cnts:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(image,(cx,cy),20,(255,255,0),10)
        distance.append(math.sqrt(((cx-image_x/2)**2)+((cy-image_y/2)**2)))
        #cv2.line(image, (cx,cy), (int(image_x/2),int(image_y/2)), [0, 255, 0], 2)
    #print(distance)
    min_value = min(distance)
    min_index = distance.index(min_value)   
    return cnts[min_index]

def get_all_contours(mask):
    ret,thresh = cv2.threshold(mask, 40, 255, 0)
    #im2,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours

# find the biggest countour (c) by the area
def get_max_contour(contours):
    c = max(contours, key = cv2.contourArea)
    return c

def process_Image(directory):
    global start_image_processing, stop_image_processing
    overall_area = []
    for filename in os.listdir(directory):
        start_image_processing = timeit.default_timer()
        if filename.endswith(".jpg"):
            image = cv2.imread(os.path.join(directory, filename))
            mask = get_lettuce_mask(image)
            # print the masked image, all lettuce
            result = cv2.bitwise_and(image, image, mask=mask) 
            #cv2.imshow( image)
            #cv2.imshow( mask)
            #cv2.imshow( result)
    
            #locate the lettuce to measure
            contours = get_all_contours(mask)
            #target_contour = get_max_contour(contours)
            try:
                target_contour = center(contours, result)
            except: 
                target_contour = get_max_contour(contours)
            #n_white_pix = np.sum(np.array(mask) > 0)#white pixel area
    
            # draw contour and bounding box on target lettuce contour
            if len(contours) != 0:
                cv2.drawContours(result, target_contour, -1, 255, 2)
                x,y,w,h = cv2.boundingRect(target_contour)
                cv2.rectangle(result,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.imwrite(os.path.join(directory+"results/", filename), result)
            
            Area =  round(100*cv2.contourArea(target_contour)/(image.shape[0]*image.shape[1]),2)
            Area = ratio_to_actual(Area)
            print("Lettuce area is {} cm".format(Area))
            overall_area.append(Area)
            # show the images
            #cv2.imshow( result)
        stop_image_processing = timeit.default_timer()
    try: size = round(sum(overall_area)/len(overall_area),2)
    except: size = 0
    print("Lettuce average size is {} cm".format(size))
    return size


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
step_sleep = 0.001
step_count = 6300 # 5.625*(1/64) per step, 4096 steps is 360°
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
    
directory = delete_img("/home/pi/Pictures0/")
cleanup()
try:
    for d in [ (False,step_count), (False,step_count), (False, step_count), (True, step_count*3)]:
        direction = d[0]
        try: takeImage(directory)
        except Exception as e: 
            print(" Can't open Camera setup...\n", e)
            time.sleep(3)
        for i in range(d[1]):
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
print("")
print("Computing the area...")
try: 
    process_Image(directory)
    print("Image processing time per image: ", stop_image_processing - start_image_processing)
except Exception as e: print(" Can't open Camera setup...\n", e)
stop_with_motor = timeit.default_timer()
print("")
print("Image processing time per image: ", stop_image_processing - start_image_processing)
print("Overall time including motor run: ", stop_with_motor - start_with_motor)



