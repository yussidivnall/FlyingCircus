#!/usr/bin/python
#from cv2 import *;
import cv2
import glob
import os
import numpy
class Faces:
    mdata_path=""
    mclassifier_path=""
    face_classifiers={
        'default'   :'haarcascade_frontalface_default.xml',
        'profile'   :'haarcascade_profileface.xml',
        'alt2'      :'haarcascade_frontalface_alt2.xml',
        'alt_tree'  :'haarcascade_frontalface_alt_tree.xml',
        'alt'       :'haarcascade_frontalface_alt.xml',
    }
    eye_classifiers={
        'eye':'haarcascade_eye.xml',
        'righteye_2splits':'haarcascade_righteye_2splits.xml',
        'lefteye_2splits':'haarcascade_lefteye_2splits.xml',
#        'mcs_righteye':'haarcascade_mcs_righteye.xml',
#        'mcs_lefteye':'haarcascade_mcs_lefteye.xml',
    }    
    actors_index={}
    model=cv2.createLBPHFaceRecognizer()
    def area(self,square):
        return square[2]*square[3]


    def get_biggest_square(self, squares):
        #print "Get biggest square"
        biggest=[0,0,0,0]
        for square in squares:
            if self.area(square) > self.area(biggest): biggest=square
        return biggest

    #get an imahe and a dictionary of classifiers
    #returns a dictionary with classifier_name:[squares]
    #example: {'mcs_lefteye':[[30,30,10,10],[50,60,20,20]]}
    def classify(self,image,classifier_dictionary):
        ret={}
        for cname,cfile_name in classifier_dictionary.iteritems():
            cpath=self.mclassifier_path+cfile_name
            classifier=cv2.CascadeClassifier(cpath)
            squares=classifier.detectMultiScale(image)
            ret[cname]=squares
        return ret

    def normalize(self,image):
        ret=cv2.resize(image,(255,255))
        ret=cv2.cvtColor(ret,cv2.COLOR_BGR2GRAY)
        return ret
    # Find some face elements, another possible check to preform...
    #
    def find_face_elements(self,face_image):
        output=face_image
        eyes=self.classify(face_image,self.eye_classifiers)
        for key,squares in eyes.iteritems():
            if len(squares) < 2:
                print "did not find 2 eyes using "+key
                continue
            for square in squares:
                color=0
                if key=='eye':color=(0,0,255)
                elif key=='righteye_2splits': color=(0,0,230)
                elif key=='lefteye_2splits':color=(0,0,205)
                elif key=='mcs_righteye':color=(0,0,180)
                elif key=='mcs_lefteye':color=(0,0,155)
                cv2.rectangle(output,(square[0],square[1]),(square[0]+square[2],square[1]+square[3]),color)
        cv2.imshow("Some name",output)
        cv2.waitKey(0)


    def index_positives(self):
        index=0
        index_file=open(self.mdata_path+"positives.csv","w")
        for directory in glob.glob(self.mdata_path+"*nm*/"):
            index+=1
            for positive_image in glob.glob(directory+"faces/positives/*.jpg"):
                line=str(index)+";"+positive_image
                print line
                index_file.write(line+"\n")
        index_file.close()

    #read positives.csv, populate actors_index dictionary with {'index':'ACTOR_NAME-IMDB_ID'}
    #example {'84':'John_Cleese-nm0000092'}
    def index_actors(self):
        f=open(self.mdata_path+"positives.csv","r")
        for line in f:
            index,file_name = line.split(';')
            if index not in self.actors_index:
                actor_id=file_name.rsplit('/',4)[1]
                self.actors_index[index]=actor_id
        f.close()
    #
    #   Get an actor index from imdb_id
    #
    def get_actor_index(self,imdb_id):
        for index,actor_id in self.actors_index.iteritems():
            if actor_id.endswith(imdb_id):return index
        else: raise Exception("No actor is indexed with imdb_id:"+imdb_id)



    #Iterate through mdata_path sub directories
    #extract faces from 'profile.jpg'
    #preform some sanity checks: 
    #-No more than 1 face per profile, if so, find biggest picture
    #-Make sure square is big enough in relation to image
    #-...(Other tests?) (centre most square?)
    #save to mdata_path/faces/positives/profile_CASCADE_NAME.jpg
    #index to mdata_path/positives.csv
    def extract_and_index_all_profiles(self):
        for profile_image_path in glob.glob(self.mdata_path+"*/profile.jpg"):
            actor_path=profile_image_path.rsplit("/",1)[0]+"/"
            image=cv2.imread(profile_image_path)
            width=image.shape[0]
            height=image.shape[1]
            faces=self.classify(image,self.face_classifiers)
            for c_name,squares in faces.iteritems():
                if squares==():continue
                square=None
                if len(squares) >1 : square=self.get_biggest_square(squares)
                else :square=squares[0]
                if self.area(square)< (0.1*width*height) : continue #Throwaway anything less than 10% of image size
                face_image=image[square[1]:(square[1]+square[3]),square[0]:square[0]+square[2]]
                norm_image=self.normalize(face_image)
                if not os.path.exists(actor_path+"faces/positives"):os.makedirs(actor_path+"faces/positives")
                save_path=actor_path+"faces/positives/profile_"+c_name+".jpg"
                cv2.imwrite(save_path,norm_image)
#                cv2.imshow("Blah",norm_image)
#                cv2.waitKey(0)
#               self.find_face_elements(face_image)
        self.index_positives()



    def extract_faces(self,imdb_id):
        self.index_actors()
        images_dir="%s*-%s*/*.jpg"%(self.mdata_path,imdb_id)
        print images_dir
        actor_index=self.get_actor_index(imdb_id)
        #model=cv2.createLBPHFaceRecognizer()
        self.model.load(self.mdata_path+"model.lbph.yaml")
#        cv2.namedWindow("positives",1)
#        cv2.namedWindow("maybes",1)
        for image_path in glob.glob(images_dir):
            if image_path.rsplit('/',1)[1]=='profile.jpg':continue
            positive_save_path=image_path.rsplit('/',1)[0]+"/faces/positives/"
            save_path=image_path.rsplit('/',1)[0]+"/faces/"
            image=cv2.imread(image_path)
            faces=self.classify(image,self.face_classifiers)
            for c_name,squares in faces.iteritems():
                if squares==():continue
                face_num=0
                for square in squares:
                    face_num+=1
                    save_file_name=image_path.rsplit('/',1)[1][:-4]+"-"+c_name+"-"+str(face_num)+".jpg"
                    positive_save_to=positive_save_path+save_file_name
                    save_to=save_path+save_file_name
                    if os.path.exists(save_to):continue;
                    face_image=image[square[1]:(square[1]+square[3]),square[0]:square[0]+square[2]]
                    cv2.imwrite(save_to,face_image)
                    norm_image=self.normalize(face_image)
                    prediction=self.model.predict(norm_image)
                    if int(prediction[0]) != int(actor_index):
                        print "predicted |"+str(prediction[0])+"| but looking for |"+str(actor_index)+"|"
                        continue
                    print str(prediction[0]) + " "+str(actor_index)
                    if int(prediction[0])==int(actor_index) and prediction[1] < 73:
                        
                        print prediction
                        print "got one"
                        cv2.imshow("positives",face_image)
                        cv2.waitKey(0)
                        cv2.imwrite(positive_save_to,norm_image)
                    elif int(prediction[0]==int(actor_index)):
                        print prediction
                        print "that's a maybe..."
                        #cv2.imshow("maybes",face_image)
                        #cv2.waitKey(0)
                        

    #train an LBPH model from indexfile mdata_path/positives.csv
    def train(self):
        images=[]
        labels=[]
        index_file=open(self.mdata_path+"positives.csv","r")
        for line in index_file:
            label,file_name=line.strip().split(';')
            labels.append(int(label))
            image=cv2.imread(file_name,cv2.IMREAD_GRAYSCALE)
            images.append(image)
        #model=cv2.createLBPHFaceRecognizer()
        self.model.train(images,numpy.asarray(labels))
        self.model.save(self.mdata_path+"model.lbph.yaml")
    
    def predict(self,image_path):
        #model=cv2.createLBPHFaceRecognizer()
        self.model.load(self.mdata_path+"model.lbph.yaml")
        image=cv2.imread(image_path)
        faces=self.classify(image,self.face_classifiers)
        for c_name,squares in faces.iteritems():
            for square in squares:
                face_image=image[square[1]:(square[1]+square[3]),square[0]:square[0]+square[2]]
                face_image=self.normalize(face_image)
                prediction=model.predict(face_image)
                print prediction

    def get_faces_from_image(self,image):
        faces=self.classify(image,self.face_classifiers)
        ret=[]
        for c_name,squares in faces.iteritems():
            for square in squares:
                face_image=image[square[1]:(square[1]+square[3]),square[0]:square[0]+square[2]]
                ret.append(face_image)
        return ret
    def predict_actor_from_face_image(self,image):
        #model=cv2.createLBPHFaceRecognizer()
        self.model.load(self.mdata_path+"model.lbph.yaml")
        prediction=self.model.predict(image)
        return prediction
    def __init__(self,data_path="/tmp/imdb/",classifier_path='/home/volcan/Desktop/development/FlyingCircus/cascade_classifiers/'):
        self.mdata_path=data_path
        self.mclassifier_path=classifier_path      
        self.index_actors()

#if __name__=='__main__':
#    mfaces=Faces()
#    mfaces.extract_and_index_all_profiles()
#    mfaces.index_positives()
#    mfaces.train()
#    mfaces.predict("/home/volcan/Desktop/development/FlyingCircus/montypython.jpg")
#     mfaces.predict("/home/volcan/Desktop/development/FlyngCircus/frame003.png")
#    mfaces.index_actors()
#    mfaces.extract_faces('nm0000092')
#    print "training..."
#    mfaces.index_positives()
#    mfaces.train()
