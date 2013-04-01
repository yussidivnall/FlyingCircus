#!/usr/bin/python
#from cv2 import *;
import cv2
import glob
import os
import numpy
class Common:
    mclassifier_path="/home/volcan/Desktop/development/FlyingCircus/cascade_classifiers/"
    face_classifiers={
        'default'   :'haarcascade_frontalface_default.xml',
        'profile'   :'haarcascade_profileface.xml',
        'alt2'      :'haarcascade_frontalface_alt2.xml',
        'alt_tree'  :'haarcascade_frontalface_alt_tree.xml',
        'alt'       :'haarcascade_frontalface_alt.xml',
    }
    @staticmethog
    def extract_faces(image)
        print type image
