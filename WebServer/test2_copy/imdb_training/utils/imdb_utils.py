#!/usr/bin/python
import urllib2
import urllib
import sys

import os
import glob
from bs4 import BeautifulSoup
class imdb_utils:
    temp_path="/tmp/imdb_training/"
    media_path="/media/actors/"
    def set_media_path(self,path):
        self.media_path=path
    def set_temp_path(self,path):
        self.temp_path=path
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
    #Retrieve actor's name
    def get_name(self,soup):
        ret=""
        for h1 in soup.findAll("h1", {'class':'header','itemprop':'name'}):
            ret=h1.find(text=True).strip()
        return ret
    #search imdb for actor
    def search(self,query):
        ret=[]
        address_template="http://www.imdb.com/find?q=%s&s=nm"
        query=query.strip().replace(' ','+')
        search_address=address_template %(query)
        soup=self.get_soup(search_address)
        #Problem here: sometimes, this search redirect stright to actor's page instead of giving search result list
        #dirty hack:
        if soup.find('td',{'id':'img_primary'}):
            imdb_id=self.get_imdb_id(soup)
            obj={'status':'found','id':imdb_id}
            ret.append(obj)
            return ret
        if soup.find('div',{'class':'findNoResults'}):
            return 'nothing'
        table=soup.find("table",{'class':'findList'})
        if (table==None): raise Exception ('actor search','could not find table with class=findList at address:'+search_address)
        for tr in table.findAll("tr"):
            img_addr=""
            actor_id=""
            actor_name=""
            actor_id=tr.find("td",{'class','primary_photo'}).find('a')['href'].strip()[6:15]
            img_addr=tr.find("td",{'class','primary_photo'}).find('img')['src']
            actor_name=tr.find("td",{'class','result_text'}).find('a').find(text=True).strip()
            obj={'id':actor_id,'name':actor_name,'img_src':img_addr}
            ret.append(obj)
        return ret
    def get_profile_image_url(self,soup):        
        #This might need to be more specific in future 'title':'name Picture'
        img=soup.find("img",{'itemprop':'image'})
        return img['src']        

    def get_all_images_urls(self,imdb_id):
        ret={}
        address_template="http://www.imdb.com/name/%s/"
        profile_page_url=address_template %(imdb_id)
        profile_soup = self.get_soup(profile_page_url)
        actor_name=self.get_name(profile_soup)
        ret['profile_image_url']=self.get_profile_image_url(profile_soup) 
        ret['images_urls']=[]
        print ret['profile_image_url']
        #Make soup for images index page (currently only first page of images)
        images_soup=self.get_soup(profile_page_url+"mediaindex")
        div = images_soup.find("div",{'class':'thumb_list'})
        for a in div.findAll('a'): #Iterate over image links
            img_page_url='http://www.imdb.com'+a['href']
            img_soup=self.get_soup(img_page_url) #Get soup of image page
            img=img_soup.find("img",{'id':'primary-img'})
            ret['images_urls'].append(img['src'])
        return ret
    
    #Generate an index of images from input path
    # ret={}
    # ret['image_name']={
    #   path:'...', src:'...',
    #   faces={fs_path:'...' , src:'...' , square=[a,b,c,d] , classifier='...'} //Not implemented at this stage, here for clarity
    # }
    def generate_image_indices(self,path):
        ret={}
        for img in glob.glob(path+"*.jpg"):
            name=img.rsplit("/",1)[1][:-4]
            path=img
            src=img.replace(self.temp_path,self.media_path)
            faces={}
            ret[name]={'path':path,'src':src,'faces':faces}
        return ret
    #Downloads all images (If not downloaded already) to 
    #temp_path/<Actor Name>-<imdb-id>.jpg
    #returns an index dictionary of images (see generate_image_indices)
    def download_all_images(self,imdb_id):
        address_template="http://www.imdb.com/name/%s/"
        profile_page_url=address_template %(imdb_id)
        profile_soup = self.get_soup(profile_page_url)
        actor_name=self.get_name(profile_soup)
        actor_name=actor_name.strip().replace(' ','_')#To handle path correctly
        data_path = self.temp_path+actor_name+"-"+imdb_id+"/"
        if not os.path.exists(data_path): 
            images_urls=self.get_all_images_urls(imdb_id)
            os.makedirs(data_path)
            self.update_actors_index_file(actor_name,imdb_id)
            urllib.urlretrieve(images_urls['profile_image_url'],data_path+"profile.jpg")
            img_num=1
            for img_url in images_urls['images_urls']:
                urllib.urlretrieve(img_url,data_path+str(img_num)+".jpg")
                img_num+=1
        return self.generate_image_indices(data_path)


    def update_actors_index_file(self,actor_name,actor_imdbid):
        actors_index_file_name=self.temp_path+"actors_index.dat"
        actor_unique_key=actor_name+"-"+actor_imdbid
        if not os.path.exists(actors_index_file_name):
            file = open(actors_index_file_name, 'w')
            file.write("1;"+actor_unique_key+"\n")
            file.close()
        else:
            f=open(actors_index_file_name)
            lines=f.readlines()
            f.close()
            actor_index=1
            for line in lines:
                words=line.split(';')
                actor_index=int(words[0])
                if(words[1]==actor_unique_key):
                    return #already indexed
            with open(actors_index_file_name,'a') as f:
                f.write(str(actor_index+1)+";"+actor_unique_key+"\n")
#if __name__=='__main__':
#    minst=imdb_utils()
#    images_index=minst.download_all_images('nm0000246')
#    for key,value in images_index.iteritems():
#        print key +" "+ value['src']+" "+value['path']
#if __name__=='__main__':
#    minst=imdb_utils()
#    images_index=minst.download_all_images('nm0000246')
#    for img in images_index['pictures']:
#        print img
#    images_urls=minst.get_all_images_urls('nm0000246')
#    print images_urls['profile_image_url']
#    for img in images_urls['images_urls']:
#        print img
     
