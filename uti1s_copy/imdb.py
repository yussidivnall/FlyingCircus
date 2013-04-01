#!/usr/bin/python
import urllib2
import urllib
import sys

import os
import glob
from bs4 import BeautifulSoup
import re
class imdb:
    mdata_path=""
    murl_root=""

    #Get soup from address
    def get_soup(self,address):
        response = urllib2.urlopen(address)
        page_source=response.read()
        response.close()
        return BeautifulSoup(page_source);

    #Get actor's imdb id from soup
    def get_imdb_id(self,soup):
        imdb_id=soup.find('link',{'rel':'canonical'})['href'][-10:-1]
        return imdb_id


    #"static", create soup and fetch name
    @staticmethod
    def get_name_from_imdbid(imdb_id):
        template="http://www.imdb.com/name/%s/"
        address=template %(imdb_id)
        inst=imdb()
        soup=inst.get_soup(address)
        name=inst.get_name(soup)
        return name

    #Get actor's name from soup
    def get_name(self,soup):
        ret=""
        for h1 in soup.findAll("h1", {'class':'header','itemprop':'name'}):
            ret=h1.find(text=True).strip()
        return ret

    def get_profile_image_url(self,soup):
        td=soup.find('td',{'id':'img_primary'})
        a=td.find('a')
        if a==None: return None #No profile image for this actor
        url_extension=a['href'].strip()
        image_page_soup=self.get_soup("http://www.imdb.com"+url_extension)
        img=image_page_soup.find('img',{'id':'primary-img'})
        return img['src'].strip()

    def get_imdb_id(self,soup):
        imdb_id=soup.find('link',{'rel':'canonical'})['href'][-10:-1]
        return imdb_id

    #Retrieve actor's name
    def get_name(self,soup):
        ret=""
        for h1 in soup.findAll("h1", {'class':'header','itemprop':'name'}):
            ret=h1.find(text=True).strip()
        return ret

    def fetch_profile_image(self,name,imdb_id,image_url):
        name=name.replace(' ','_').strip()
        save_path=self.mdata_path+name+"-"+imdb_id+"/"
        if not os.path.exists(save_path): 
            os.makedirs(save_path)
            urllib.urlretrieve(image_url,save_path+"profile.jpg")
        print save_path

    #Retrieve a list of the first 100 actors in imdb
    #fetch their profile picture
    #store in mdata_path/ACTOR_NAME-IMDBID/profile.jpg
    def fetch_initial_learning_faces(self):
        for i in range(1,101):
            imdb_id="nm%07i"%(i)
            actor_page="http://www.imdb.com/name/%s"%(imdb_id)
            profile_page_soup=self.get_soup(actor_page)
            name=self.get_name(profile_page_soup).strip()
            profile_image_url=self.get_profile_image_url(profile_page_soup)
            if profile_image_url==None:
                print "No Profile Image"
                continue
            print name+" "+imdb_id+" "+actor_page+" "+profile_image_url
            self.fetch_profile_image(name,imdb_id,profile_image_url)
    def get_all_images_urls(self,soup,media_index_url):
        ret=[]
        div=soup.find("div",{'class':'thumb_list'})
        for a in div.findAll('a'):
            img_page_url='http://www.imdb.com'+a['href']
            img_soup=self.get_soup(img_page_url) #Get soup of image page
            img=img_soup.find("img",{'id':'primary-img'})
            ret.append(img['src'])
        a=soup.find("a",text=re.compile("Next "))
        if a !=None: 
            print "More pictures"
            new_soup=self.get_soup(media_index_url+a['href'])
            more_images=self.get_all_images_urls(new_soup,media_index_url)
            for img in more_images:
                ret.append(img)
        else : print "no more pages"
        return ret

    def fetch_all_images(self,imdb_id):
        actor_page="http://www.imdb.com/name/%s"%(imdb_id)
        profile_page_soup=self.get_soup(actor_page)
        actor_name=self.get_name(profile_page_soup).strip().replace(" ","_")
        actor_path=self.mdata_path+actor_name+"-"+imdb_id+"/"
        print actor_path
        if not os.path.exists(actor_path+"profile.jpg"): #If we don't already have this actor...
            profile_image_url=self.get_profile_image_url(profile_page_soup)
            if profile_image_url==None:raise Exception("Failed to find profile image for "+actor_name+" imdb_id "+imdb_id)
            self.fetch_profile_image(name,imdb_id,profile_image_url)
        pictures_soup=self.get_soup(actor_page+"/mediaindex")
        print "Getting all images urls"
        images_urls=self.get_all_images_urls(pictures_soup,actor_page+"/mediaindex")
        
        print "Downloading all images"
        image_num=0
        for image_url in images_urls:
            image_num+=1
            urllib.urlretrieve(image_url,actor_path+str(image_num)+".jpg")




    def __init__(self,data_path="/tmp/imdb/",url_root="/imdb/"):
        self.mdata_path=data_path
        self.murl_root=url_root

#if __name__=='__main__':
#    mimdb=imdb()
#    mutils.fetch_initial_learning_faces()
#    mimdb.fetch_all_images("nm0000092")    
