#!/usr/bin/python
import cv
from cv import *;
import cv2
from cv2 import *;
import numpy;
import sys, os
import argparse
import string
import glob
import pickle
import imdb_utils #For testing only...
import pprint

class face_utils:
    classifier_path="/home/volcan/Desktop/development/FlyingCircus/WebServer/media/classifiers/"
    classifiers=[]
    media_path="/media/actors/"
    temp_path="/tmp/imdb_training/"
    def populate_classifiers(self):
        for classifier in glob.glob(self.classifier_path+"*.xml"):
            self.classifiers.append(classifier)
    def set_classifier_path(self,path):
        self.classifier_path=path
    def set_temp_path(self,path):self.temp_path=path
    def set_media_path(self,path):self.media_path=path

#
#   Returns squares in 'image' which match 'classifier'
#
    def classify(self,image,cascade):
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
#   returns the image inside the square
#
    def get_square_from_image(self,image,square):
        ret=cv.GetSubRect(image,square[0])
        return ret
#
#   extracts all images which were caught by all classifiers, save an index of faces
#

    def extract_from_index(self,image_indices):
        self.populate_classifiers()
        save_root_path=image_indices['profile']['path'].rsplit('/',1)[0]+"/faces/"
        index_file=save_root_path+"index.dat"
        
        if not os.path.exists(save_root_path):
            os.makedirs(save_root_path)
        elif os.path.isfile(index_file):
            print "Found index file... loading instead"
            ret=pickle.load(open(index_file,'rb'))
            return ret
            
        print save_root_path
        ret=image_indices
        for key,value in image_indices.iteritems(): #Iterate over image index
            ret[key]['faces']={}
            image=cv.LoadImage(value['path'],cv.CV_LOAD_IMAGE_COLOR)
            for cpath in self.classifiers: #Iterate over classifiers
                classifier_name=cpath.rsplit("/",1)[1][:-4]
                face_root_name=key+"-"+classifier_name
                classifier=cv.Load(cpath)
                squares=self.classify(image,classifier)
                if(squares): #if faces found
                    face_num=1
                    for square in squares: #iterate over each detected face
                        face_name=face_root_name+"-face-"+str(face_num)
                        file_name=save_root_path+face_name+".jpg"
                        url=file_name.replace(self.temp_path,self.media_path)
                        square_image=self.get_square_from_image(image,square)
                        cv.SaveImage(file_name,square_image)
                        print url
                        ret[key]['faces'][face_name]={
                            'classifier':classifier_name,
                            'square':square,
                            'src':url,
                            'fs_path':file_name
                        }
                        face_num+=1
        pickle.dump(ret,open(index_file,'wb'))
        return ret
    
    def resize(img,size):
        ret=cv2.resize(img,size)
        return ret
    def fischer_train(self,image_indices,positives):
        model=createFisherFaceRecognizer();
        labels=[]
        images=[]
        label=0
        for key,val in image_indices.iteritems():
            for k1,face in val['faces'].iteritems():
                if k1 in positives:
                    img=cv2.imread(face['fs_path'],cv2.IMREAD_GRAYSCALE)
                    img=resize(img,(256,256))
                    #print k1+" is a positive match in "+face['fs_path']
                    labels.append(label)
                    images.append(numpy.asarray(img,dtype=numpy.uint8))
                    #label+=1
        model.train(images,numpy.asarray(labels))
        #labels_numpy=numpy.array(label)
        #images_numpy=numpy.array(images)
        #model.train(labels_numpy,images_numpy)
        return model


    def set_positives(self,image_indices,positives):
        ret=image_indices
        for pkey,picture in image_indices.iteritems():
            for fkey,face in picture['faces'].iteritems():
                if fkey in positives:
                    ret[pkey]['faces'][fkey]['positive']=True
        return ret

#
#   Get actors index as dictionary
#   ret[index]=actor_name-imdbid
#
    def actors_index_dictionary(self):
        f=open(self.temp_path+"actors_index.dat")
        lines=f.readlines()
        f.close()
        ret={}
        for line in lines:
            words=line.split(";")
            index=int(words[0])
            unique_id=words[1].strip()
            ret[index]=unique_id
        return ret

    #loads (returns) an images indices dictionary given an imdb_id
    def image_indices_from_imdb_id(self,imdb_id):
        paths=glob.glob(self.temp_path+"*"+imdb_id+"/faces/index.dat")
        if len(paths) != 1: raise Exception("Too many imdb_ids: "+imdb_id)
        ret=pickle.load(open(paths[0],'rb'))
        return ret

    #saves an updated image indices to actor with imdb_id
    def save_image_indices(self,image_indices,imdb_id):       
        paths=glob.glob(self.temp_path+"*"+imdb_id+"/faces/index.dat")
        if len(paths) != 1: raise Exception("Too many imdb_ids: "+imdb_id)
        pickle.dump(image_indices,open(paths[0],'wb'))

#   trains a new local binary patterns histogram
#   goes over self.temp_path/actor_index.dat
#   for each actor, load indices, get positives, and train
#   save to self.temp_path/model.lbph.yaml    
    def train_lbph(self):
        faces_path_template=self.temp_path+"%s/faces/index.dat"
        positives=[]
        labels=[]
        index_file_path=self.temp_path+"actors_index.dat"
        if not os.path.isfile(index_file_path):
            raise Exception("Missing actors index file??!")
        index_file=open(index_file_path,'r') 
        lines=index_file.readlines()
        index_file.close()
        for line in lines:
            words=line.split(';')
            label=words[0]
            actor_unique_id=words[1].strip()
            face_indices_path=faces_path_template %(actor_unique_id)
            image_indices=pickle.load(open(face_indices_path,'rb'))
            for pkey,picture in image_indices.iteritems():
                for fkey,face in picture['faces'].iteritems():
                    if 'positive' in face and face['positive']:
                        positives.append(face['fs_path'])
                        labels.append(int(label))
        positive_array=[]
        for image_path in positives:
            img=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
            img=resize(img,(256,256))
            positive_array.append(img)
        model=createLBPHFaceRecognizer();
        model.train(numpy.asarray(positive_array,numpy.uint8),numpy.asarray(labels))
        model.save(self.temp_path+"model.lbph.yaml")
#
#   Load lbph model, for each face in image_indices, append an lbph_label and lbph_confidence
#
    def predict_lbph_labels(self,image_indices):
        model=createLBPHFaceRecognizer()
        model.load(self.temp_path+"model.lbph.yaml")
        ret=image_indices
        index=self.actors_index_dictionary()
        for pkey,picture in image_indices.iteritems():
            for fkey,face in picture['faces'].iteritems():        
                img=cv2.imread(face['fs_path'],cv2.IMREAD_GRAYSCALE) 
                img=resize(img,(256,256))
                prediction=model.predict(numpy.asarray(img))
                label_num=prediction[0]
                label_name=index[label_num]
                ret[pkey]['faces'][fkey]['lbph_label']=label_name
                ret[pkey]['faces'][fkey]['lbph_confidence']=prediction[1]
        return ret
                
#   trains all models
#   goes over self.temp_path/actor_index.dat
#   for each actor, load indices, get positives, and train
#   save to self.temp_path/model.model_name.yaml    
    def train_all(self):
        faces_path_template=self.temp_path+"%s/faces/index.dat"
        positives=[]
        labels=[]
        index_file_path=self.temp_path+"actors_index.dat"
        if not os.path.isfile(index_file_path):
            raise Exception("Missing actors index file??!")
        index_file=open(index_file_path,'r') 
        lines=index_file.readlines()
        index_file.close()
        for line in lines:
            words=line.split(';')
            label=words[0]
            actor_unique_id=words[1].strip()
            face_indices_path=faces_path_template %(actor_unique_id)
            image_indices=pickle.load(open(face_indices_path,'rb'))
            for pkey,picture in image_indices.iteritems():
                for fkey,face in picture['faces'].iteritems():
                    if 'positive' in face and face['positive']:
                        positives.append(face['fs_path'])
                        labels.append(int(label))
        positive_array=[]
        for image_path in positives:
            img=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
            img=resize(img,(256,256))
            positive_array.append(img)
        lbph_model=createLBPHFaceRecognizer();
        lbph_model.train(numpy.asarray(positive_array,numpy.uint8),numpy.asarray(labels))
        lbph_model.save(self.temp_path+"model.lbph.yaml")

        fisher_model=createFisherFaceRecognizer();
        fisher_model.train(numpy.asarray(positive_array,numpy.uint8),numpy.asarray(labels))
        fisher_model.save(self.temp_path+"model.fisher.yaml")

        eigen_model=createEigenFaceRecognizer();
        eigen_model.train(numpy.asarray(positive_array,numpy.uint8),numpy.asarray(labels))
        eigen_model.save(self.temp_path+"model.eigen.yaml")
#
#   Load all models, for each face in image_indices, append an <model>_label and <model>_distance
#
    def predict_all_labels(self,image_indices):
        lbph_model=createLBPHFaceRecognizer()
        lbph_model.load(self.temp_path+"model.lbph.yaml")

        fisher_model=createFisherFaceRecognizer()
        fisher_model.load(self.temp_path+"model.fisher.yaml")

        eigen_model=createEigenFaceRecognizer()
        eigen_model.load(self.temp_path+"model.eigen.yaml")
        ret=image_indices
        index=self.actors_index_dictionary()
        for pkey,picture in image_indices.iteritems():
            for fkey,face in picture['faces'].iteritems():        
                img=cv2.imread(face['fs_path'],cv2.IMREAD_GRAYSCALE) 
                img=resize(img,(256,256))

                lbph_prediction=lbph_model.predict(numpy.asarray(img))
                fisher_prediction=fisher_model.predict(numpy.asarray(img))
                eigen_prediction=eigen_model.predict(numpy.asarray(img))

                ret[pkey]['faces'][fkey]['lbph_label']=index[lbph_prediction[0]]
                ret[pkey]['faces'][fkey]['fisher_label']=index[fisher_prediction[0]]
                ret[pkey]['faces'][fkey]['eigen_label']=index[eigen_prediction[0]]


                ret[pkey]['faces'][fkey]['lbph_distance']=lbph_prediction[1]
                ret[pkey]['faces'][fkey]['fisher_distance']=fisher_prediction[1]
                ret[pkey]['faces'][fkey]['eigen_distance']=eigen_prediction[1]

        return ret
    def train_fisherfaces(self):
        pass

    def train_eigenfaces(self):
        pass
    def update_lbph_model(self,imdb_id):
        pass

def init():
    minst=face_utils()
    minst.set_temp_path('/home/volcan/Desktop/development/FlyingCircus/WebServer/media/actors/')
    minst.train_all()
    image_index=minst.image_indices_from_imdb_id('nm0000093')
    image_index=minst.predict_all_labels(image_index)
    for pkey,picture in image_index.iteritems():
        for fkey,face in picture['faces'].iteritems():
            print str("LBPH: "+face['lbph_label'])+" "+str(face['lbph_distance'])
            print str("Fisher: "+face['fisher_label'])+" "+str(face['fisher_distance'])
            print str("Eigen: "+face['eigen_label'])+" "+str(face['eigen_distance'])


#    minst.image_indices_from_imdb_id('nm0000246')



#    mimdb_utils=imdb_utils.imdb_utils()
#    images_index=mimdb_utils.download_all_images('nm0000246')
#    minst=face_utils()
#    images_index=minst.extract_from_index(images_index)
#    positives=['24-haarcascade_frontalface_alt-face-1','25-haarcascade_frontalface_alt-face-1','20-haarcascade_frontalface_alt-face-1']
#    model=minst.lbph_train(images_index,positives)
#    image_index=minst.label_confidence(model,images_index)



#    for key,val in images_index.iteritems():
#        predicted_label=-1
#        predicted_confidence=0.0
#        r=model.predict(numpy.asarray(cv2.imread(val['path'],cv2.IMREAD_GRAYSCALE)))
#        print r
#        for k1,face in val['faces'].iteritems():
#            img=cv2.imread(face['fs_path'],cv2.IMREAD_GRAYSCALE)
#            p=model.predict(numpy.asarray(img))
#            print "Face "+k1+" "+unicode(p)
#        #print key+" "+predicted_label+" "+predicted_confidence
if __name__=='__main__': init()
