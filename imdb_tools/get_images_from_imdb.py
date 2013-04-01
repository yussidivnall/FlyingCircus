#!/usr/bin/python
#Retrive an actor imdb_id,name,profile_image and images from first page of actor's images
#stores in datadir/name-imdb_id/profile.jpg and  datadir/name-imdb_id/1.jpg,2.jpg...
#from imdb

import urllib2
import urllib
import sys

import os
from bs4 import BeautifulSoup
#address='http://www.imdb.com/name/nm0000246/' #Bruce willis
datadir='./data/'
address='http://www.imdb.com/name/nm0000424/' #Hugh Grant


class Actor():
    imdb_id=-1
    name=''
    profile_image_url=''
    images_urls=[]


#Gets the imdb actor id from address
def get_imdb_id(address):
    return address[-10:-1]

#Find the address of "images page", 
#retrive it and download all images
def get_all_images():
    print ("Getting image addresses")
    global address
    ret=[]
    #Make soup for images index page (currently only first page of images)
    soup=get_soup(address+"mediaindex")
    div = soup.find("div",{'class':'thumb_list'})
    for a in div.findAll('a'):
        image_page_address='http://www.imdb.com'+a['href']
        #Get a soup for each individual image page
        image_soup=get_soup(image_page_address)
        img=image_soup.find("img",{'id':'primary-img'})
        ret.append(img['src'])
    return ret

#Gets the profile image url from page
def get_profile_image(soup,name):
    #This might need to be more specific in future 'title':'name Picture'
    img=soup.find("img",{'itemprop':'image'})
    return img['src']        

#Get's the actor's name from the imdb page
def get_name(soup):
    ret=""
    for h1 in soup.findAll("h1", {'class':'header','itemprop':'name'}):
        ret=h1.find(text=True).strip()
    return ret

def get_soup(address):
    response = urllib2.urlopen(address)
    page_source=response.read()
    response.close()
    return BeautifulSoup(page_source);


def init():
    global address;
    global datadir
    actor=Actor() 
    actor.imdb_id=get_imdb_id(address)
    soup=get_soup(address)
    actor.name=get_name(soup)   
    actor.profile_image_url=get_profile_image(soup,actor.name)
    actor.images_urls=get_all_images()
    data_path = datadir+actor.name+"-"+actor.imdb_id+"/"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    
    print ("Downloading images")
    urllib.urlretrieve(actor.profile_image_url, data_path+"profile.jpg")
    index=1
    for img_addr in actor.images_urls:
        urllib.urlretrieve(img_addr,data_path+str(index)+".jpg")
        index+=1

if __name__=='__main__': init()
