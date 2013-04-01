#!/usr/bin/python
#ref:http://www.bytefish.de/blog/face_recognition_with_opencv2
import os,sys,numpy
import PIL.Image as Image
def read_images(path,person_index,sz=None):
    images=[]
    labels=[]
    for filename in os.listdir(path):
        im=Image.open(os.path.join(path,filename))
        im=im.convert("L")
        if (sz is not None):
            im=im.resize(sz,Image.ANTIALIAS)
        images.append(numpy.asarray(im,dtype=numpy.uint8))
        labels.append(0)
    labels=numpy.asarray(labels)
    return [images,labels]

if __name__=="__main__":
    D=read_images("normalised_positives",0)
    
