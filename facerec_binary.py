#!/usr/bin/python
#ref:http://www.bytefish.de/pdf/facerec_python.pdf
import numpy
import cv2
from cv2 import *
import cv
import sys
import util
#import cv
#createFisherFaceRecognizer();
model=createLBPHFaceRecognizer();
images=[]
labels=[]

def main():
    global model
    imgs=util.read_images("normalised_positives",0)
    model.train(imgs[0],imgs[1] )
    model.save("what.who")
if __name__=="__main__":main()


