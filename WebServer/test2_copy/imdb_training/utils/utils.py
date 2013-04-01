#!/usr/bin/python
import urllib2
import urllib
import sys

import os
from bs4 import BeautifulSoup
class utils:
    def get_soup(self,address):
        response = urllib2.urlopen(address)
        page_source=response.read()
        response.close()
        return BeautifulSoup(page_source);


    def search(self,query):
        ret=[]
        address_template="http://www.imdb.com/find?q=%s&s=nm"
        query=query.strip()
        search_address=address_template %(query)
        soup=self.get_soup(search_address)
        table=soup.find("table",{'class':'findList'})
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
if __name__=='__main__':
    minstance=utils();
    list_of_actors=minstance.search("john+smith")
    for obj in list_of_actors:
        print obj['id']+" "+obj['name']
