#!/usr/bin/python
import urllib2
import urllib
import sys
import json

import os
import glob
from bs4 import BeautifulSoup
import re
from imdb import imdb
from faces import Faces
class GoogleImages:
    mdata_path=""
    murl=""
    mfaces=None


    #retrieve actor name from imdbid, search google images,
    #store images to mdata_path/ACTOR_NAME-IMDBID
    def search(self,actor_imdbid,num_images=500): 
        name=imdb.get_name_from_imdbid(actor_imdbid)
        query_name=name.replace(" ","+")+"+actor"
        path_name=name.replace(" ","_")+"-"+actor_imdbid+"/"
        print path_name #Actor_Name-imdbid

        if not os.path.exists(self.mdata_path+path_name): os.makedirs(self.mdata_path+path_name)
        address_template='https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+query_name+'&start=%d'
        for start in range(0,61,4):
            try:
                response=urllib2.urlopen(address_template %start)
                response_text=response.read()
                response.close()
                results=json.loads(response_text)['responseData']['results']
            except Exception, e:
                print "could not get "+address_template %start
                continue
            pos=1
            for result in results:
                index=start+pos
                image_url=result['unescapedUrl']
                image_name=image_url.rsplit('/',1)[1]
                print image_name
                pos+=1
                urllib.urlretrieve(image_url,self.mdata_path+path_name+str(index)+image_name)
    #Extract all faces in directory of actor imdbid
    #
    def extract_faces(self,imdb_id):
        actor_path=glob.glob(self.mdata_path+"*"+imdb_id+"*")[0]+"/"
        if not os.path.exists(actor_path+"faces"):
            os.makedirs(actor_path+"faces")
        
    #Train Haar cascade for actor imdbid
    #
    def train_haar(self,actor_imdbid):pass

    #Train all actor's LBPH face recognizer (update?)
    #
    def train_faces_recognizer(self):pass


    def __init__(self,data_path="/tmp/flyingCircus/google/", url_root="/flyingcircus/google/"):
        self.mdata_path=data_path
        self.murl_root=url_root
        self.mfaces=Faces("/tmp/flyingCircus/google/")

if __name__=='__main__':
    mgoogle=GoogleImages()
#    mgoogle.search("nm0000092")
    mgoogle.extract_faces("nm0000092")
