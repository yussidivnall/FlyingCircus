#!/usr/bin/python
#
# Extract all objects classified by a given cascade classifier from an image
#
import cv
from cv import *;
import cv2
import numpy;
import sys, os
import argparse

storage = cv.CreateMemStorage(0)



def classify(img_path,cc_path):
    global storage;
    image=cv.LoadImage(img_path, cv.CV_LOAD_IMAGE_COLOR)
    cascade=cv.Load(cc_path);

    min_size = (20, 20)
    image_scale = 2
    haar_scale = 1.2
    min_neighbors = 2
    haar_flags = 0

    faces = cv.HaarDetectObjects(image, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
    if(len(faces)==0):
        print("No objects detected");
        exit(1);
    print(len(faces));
    return faces;

#
#   %progname -i <input file> -o <output file> -c <cascade classifier> [options]
#
def main():
    parser = argparse.ArgumentParser(description="Run a cascade classifier on an image and output matched regions to new images")
    parser.add_argument("-i",action="store",dest="input_image",required=True)
    parser.add_argument("-o",action="store",dest="output",required=True)
    parser.add_argument("-c",action="store",dest="cascade_classifier",required=True)
    args = parser.parse_args()
    faces=classify(args.input_image,args.cascade_classifier)
    
    cv.WaitKey(0);

if __name__=='__main__': main()
#For Later:
#sub = cv.GetSubRect(img, (60, 70, 32, 32))  # sub is 32x32 patch within img
