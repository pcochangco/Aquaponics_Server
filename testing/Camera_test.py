import pixellib
from pixellib.semantic import semantic_segmentation
import numpy as np
import cv2
import os

def moveCamera():
 
def ratio_to_actual(image_pixel_ratio):

def takeImage():
    from picamera import PiCamera
    from time import sleep
    camera = PiCamera()
    time.sleep(2)
    camera.resolution = (1280, 720)
    camera.vflip = True
    camera.contrast = 10
    file_name = "/home/pi/Pictures/img_" + str(time.time()) + ".jpg"
    camera.capture(file_name)
    print("Picture taken.")

segment_image = semantic_segmentation()
segment_image.load_ade20k_model("/deeplabv3_xception65_ade20k.h5")
directory = "/home/pi/Pictures/"
overall_ratio = []
for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        ratio = 0
        segvalues, output = segment_image.segmentAsAde20k(os.path.join(directory, filename), overlay = True)
        for item in ["plant", "tree", "grass"]:
            if item in segvalues["class_names"]:
                 ratio = ratio + segvalues["ratios"][segvalues["class_names"].index(item)]
        overall_ratio.append(ratio)
        cv2.imshow(output)
image_pixel_ratio = round(sum(overall_ratio)/len(overall_ratio),2)
print("Average ratio of image to image pixel is", image_pixel_ratio)
size = ratio_to_actual(image_pixel_ratio)
print("Image size is", size)
        
