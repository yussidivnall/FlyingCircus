#!/usr/bin/python
import numpy
import cv2
from cv2 import *
import cv
#createFisherFaceRecognizer();
model=createFisherFaceRecognizer();

images=[]
labels=[]

    

def main():
    global images
    global labels
    global model

    f=open("./normalised_positives.txt")

    #For some reason, labels is a numpy array...
    #Label num of each person
    label=0 
    for line in f:
        img=imread(line,0) 
        #fileName = line[0:len(line)-1] # remove the '\n'
        #img=cv.LoadImage(fileName)
        images.append(img) 
        labels.append(0)
        #label+=1 #We're only dealing with one person
    
    labels_numpy=numpy.array(labels)
    images_numpy=numpy.array(images)
    model.train(images_numpy,labels_numpy)

if __name__=="__main__":main()
