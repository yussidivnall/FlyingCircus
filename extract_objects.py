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
import string
image=0;
cascade="";


def classify():
    global image;
    global cascade
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

def extractimages(squares):
    global image;
    images=[];
    for square in squares:
        print(square);
        square_image=cv.GetSubRect(image,square[0]);
        cv.ShowImage("SomeName",square_image);
        cv.WaitKey(0);
        images.append(square_image);
    return images;
def saveimages(path,images):
    for i in range(0,len(images)):
        filename=""+path + "/Object"+str(i)+".png"
        cv.SaveImage(filename,images[i])
        print (filename)
        print ("Image num:",i);
    pass;

#
#   %progname -i <input file> -o [output file] -c <cascade classifier> [options]
#
def main():
    global image
    global cascade
    parser = argparse.ArgumentParser(description="Run a cascade classifier on an image and output matched regions to new images")
    parser.add_argument("-i",action="store",dest="input_image",required=True)
    parser.add_argument("-o",action="store",dest="output")
    parser.add_argument("-c",action="store",dest="cascade_classifier",required=True)
    args = parser.parse_args()

    image=cv.LoadImage(args.input_image, cv.CV_LOAD_IMAGE_COLOR)
    cascade=cv.Load(args.cascade_classifier);
    cv.ShowImage("SomeName",image);
    cv.WaitKey(0);

    squares=classify();
    images=extractimages(squares);
    if (args.output):
        print ("Saving to"+args.output);
        saveimages(args.output,images);
        

if __name__=='__main__': main()
#For Later:
#sub = cv.GetSubRect(img, (60, 70, 32, 32))  # sub is 32x32 patch within img
#cv.SaveImage("fn.png",img)
