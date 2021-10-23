import pixellib
from pixellib.semantic import semantic_segmentation
from pixellib.instance import instance_segmentation
import numpy as np
import cv2
import os

def moveCamera():

def takeImage():


segment_image = semantic_segmentation()
segment_image.load_ade20k_model("/deeplabv3_xception65_ade20k.h5")
directory = "images addr to segment"
for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        ratio = 0
        segvalues, output = segment_image.segmentAsAde20k(os.path.join(directory, filename), overlay = True)
        for item in ["plant", "tree", "grass"]:
            if item in segvalues["class_names"]:
                 ratio = ratio + segvalues["ratios"][segvalues["class_names"].index(item)]
        print("Image ratio to area is {}%".format(round(ratio),2))
        cv2.imshow(output)
