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

def delete_img(folder):
    try:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except:
                folder = "/home/pi/Pictures0_" + str(time.time()) +"/"
                os.mkdir(folder)
                break
    except: os.mkdir(folder)
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
    return image_pixel_ratio

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
    overall_area = []
    for filename in os.listdir(directory):
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
            Area =  round(100*cv2.contourArea(target_contour)/(image.shape[0]*image.shape[1]),2)
            Area = ratio_to_actual(Area)
            print("Lettuce area is {} cm".format(Area))
            overall_area.append(Area)
            # show the images
            #cv2.imshow( result)
            cv2.imwrite(os.path.join("/home/pi/results", filename), result)
    size = round(sum(overall_area)/len(overall_area),2)
    print("Lettuce average size is {} cm".format(size))
    return size
    
directory = "/home/pi/Pictures0/"
results_path = "/home/pi/results"
directory = delete_img(directory)
delete_img(results_path)
takeImage(directory)
process_Image(directory)
