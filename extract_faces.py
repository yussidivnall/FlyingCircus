#!/usr/bin/python
#
# Extract all objects classified by a given cascade classifier from a directory of images
#
import cv
import sys, os
import argparse

#from cv import *

def RetriveByClassifier(src_image,dest_directory,classifier):
    
    cascade = cv.Load(classifier);
    print("RetByClass\n");
    if(cascade):
        pass;
    


def main():
    parser = OptionParser(usage = "usage: %prog [options]")
    parser.add_option("-i","--inputdirectory",action="store",type="string",dest="input_dir");
    parser.add_option("-o","--outputdirectory",action="store",type="string",dest="output_dir");
    parser.add_option("-c","--cascadeclassifier",action="store",type="string",dest="input_dir");
    print("Main\n");
    #img=cv.LoadImageM("images/Gaddafi.png");
    #cv.ShowImage("Image", img);
    #classifier="haarcascade_frontalface_alt.xml"
    #output_path = "output/"
    #RetriveByClassifier(img,output_path,classifier)
    while True:
        #cv.WaitKey(0);
        if cv.WaitKey(0) ==27:
            break;

if __name__=='__main__': main()
