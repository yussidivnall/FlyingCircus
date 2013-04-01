#!/usr/bin/python
import cv2
import numpy;
import sys, os
class Face():
    bounds=(-1,-1,-1,-1)
    left_eye=(-1,-1,-1,-1)
    right_eye=(-1,-1,-1,-1)
    mouth=(-1,-1,-1,-1)
    nose=(-1,-1,-1,-1)

class Profile():
    profile_image=None
    face=Face()
    def get_face():
        pass
    def get_eyes():
        pass
    def get_nose():
        pass
    def get_mouth():
        pass


    def __init__(self,profile_image_path):
        self.profile_image=cv2.imread(profile_image_path)


if __name__=='__main__':
    profile=Profile('./samples/profile.jpg')
    key=-1
    while key < 0:
        cv2.imshow("win1",profile.profile_image)
        key=cv2.waitKey(0)
