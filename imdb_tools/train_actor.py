#!/usr/bin/python
#
#   NOT DONE
#   This takes in a directory created by get_images_from_imdb.py
#   It looks for the profile picture (profile.jpg)
#   Runs several face extraction harr cascades on it
#   extracts the recognised faces and normailse them
#   trains a Fischer face recognisel
#   runs the Harr cascades again on the rest of the images
#   extract faces
#   and tried to match those with the profile #


import cv
from cv import *;
import cv2
import numpy;
import sys, os
import argparse
import string
import glob


profile_image=None
cascade_path="/home/volcan/Desktop/development/FlyingCircus/cascade_classifiers/"
cascades=[
    cascade_path+"haarcascade_frontalface_alt2.xml",
    cascade_path+"haarcascade_frontalface_alt_tree.xml",
    cascade_path+"haarcascade_frontalface_alt.xml",
    cascade_path+"haarcascade_profileface.xml",
]


#
#   Returns squares in 'image' which match 'classifier'
#
def classify(image,cascade):
    min_size=(20,20)
    image_scale = 2
    haar_scale = 1.9
    min_neighbors = 2
    haar_flags = 0
    ret = cv.HaarDetectObjects(image, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
    if(len(ret)==0):return None
    else: return ret

#
# Gets an image, a list of squares and return 
# a list of images in those squares
#
def extract_images(image,squares):
    images=[];
    for square in squares:
        square_image=cv.GetSubRect(image,square[0]);
        images.append(square_image);
    return images;

#
# Gets a title, array of images and display them one by one
#
def display_images(text, images):
    for img in images:
        cv.ShowImage(text,img);
        cv.WaitKey(0);

#
# Save image
#
def saveimages(path,images):
    for i in range(0,len(images)):
        filename=""+path + ".face"+str(i)+".png"
        cv.SaveImage(filename,images[i])
        print (filename)
        print ("Image num:",i);
#
#
#
def init():
    global profile_image
    parser = argparse.ArgumentParser(description="""
        Run a varius face cascade 
        classifier on a directory of images and 
        output matched regions to new images
    """)
    parser.add_argument("-i",action="store",dest="image_dir",required=True)
    parser.add_argument("-o",action="store",dest="output")
    args = parser.parse_args()
    profile_image=cv.LoadImage(args.image_dir+"profile.jpg",cv.CV_LOAD_IMAGE_COLOR)
    cv.ShowImage("SomeName",profile_image);
    cv.WaitKey(0);
    for cpath in cascades:
        print cpath
        cascade=cv.Load(cpath)
        face_squares=classify(profile_image,cascade)
        if (face_squares==None):
            print "No faces detected"
        elif (len(face_squares)==1):
            images = extract_images(profile_image,face_squares)
            display_images("Something",images)
        else:
            print str(len(face_squares))+" faces detected in profile image, should be 1"
        
if __name__=='__main__': init()
