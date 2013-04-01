#!/usr/bin/python
from faces import Faces
import cv2
import os
class Video:
    mdata_path=""
    mfaces=None
   
    def get_actor_from_video(self,video_file_path,imdb_id):
        actor_index=self.mfaces.get_actor_index(imdb_id)
        actor_id=self.mfaces.actors_index[actor_index]
        print actor_index+" "+actor_id
        capture=cv2.VideoCapture(video_file_path)
        cv2.namedWindow("input")
        while(True):
            f, img = capture.read()
            faces=self.mfaces.get_faces_from_image(img)
            for face in faces:
                face=self.mfaces.normalize(face)
                prediction=self.mfaces.predict_actor_from_face_image(face)
                print prediction
                if int(prediction[0])==int(actor_index):
                    cv2.imshow("input",face)
                    cv2.waitKey(1)
            #img=self.mfaces.normalize(img)
            #prediction=self.mfaces.predict_actors_from_image(img)
            #print prediction
            #cv2.imshow("input", img)
            #cv2.waitKey(1)

    def __init__(self,faces,data_path="/tmp/videos/"):
        self.mdata_path=data_path
        self.mfaces=faces
        self.mfaces.index_actors()
        if not os.path.exists(self.mdata_path):
            os.makedirs(self.mdata_path)
if __name__=='__main__':
    mfaces=Faces()
    mfaces.train()
    mvideo=Video(mfaces)
#    mvideo.get_actor_from_video("/home/volcan/Desktop/development/FlyingCircus/videos/JohnCleese/John_Cleese_Carefully_Considers_Your_Futile_Comments.avi"
    mvideo.get_actor_from_video("/home/volcan/Desktop/development/FlyingCircus/videos/JohnCleese/The_Brain.flv"
                                ,"nm0000092")
