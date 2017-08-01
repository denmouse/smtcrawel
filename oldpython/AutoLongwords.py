# -*- coding: cp936 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import codecs
import sys
from ctypes import windll

from lxml import *
import lxml.html
import urllib2
from urllib2 import Request, urlopen, URLError
import lxml.html as H
from lxml.html import fromstring, tostring
from lxml import etree


class Queue(object):
    def __init__(self):
        self.queue = []
        
    def en_queue(self, item):
        self.queue.append(item)

    def de_queue(self):
        if self.queue != []:
            return self.queue.pop(0)
        else:
            return None
    def head(self):
        if self.queue != []:
            return self.queue[0]
        else:
            return None

    def tail(self):
        if self.queue != []:
            return self.queue[-1]
        else :
            return None

    def length(self):
        return len(self.queue)
    
    def is_empty(self):
        return self.queue == []

def writelist(filename, outlist):
    outfile = file(filename,'wb')
    writer = csv.writer(outfile)
    for data in outlist:
        orders = data[9];
        count = orders.count('(0)')
        if count > 9 :
            continue
        writer.writerow(data)
    outfile.close()
    
def list2str(liststore):
    txt = ''
    total=0
    for lis in liststore:
        count = liststore.count(lis)
        if(count>2):
            txtcount =  ',(' + lis+': '+str(count)+')'
            if lis not in txt:
                txt = txt + txtcount
                total = total+1
    totalstr = " total :" + str(total) + ', '
    txt = totalstr + txt
    
    return txt

def readorder_ofkey(key):
    ordesless =['0', '1', '2', '3']
    url_qs = Queue()
    
    storelist = []
    outstr = ''
    
    if browser is None:
        print "browser is not open!"
        return
    try:
        browser.get("http://www.aliexpress.com")
    except:
        return ''
    
    time.sleep(1)

    keyword = key[7]
    browser.find_element_by_class_name("search-key").clear()
    browser.find_element_by_class_name("search-key").send_keys(keyword)
    browser.find_element_by_class_name("search-key").send_keys(Keys.ENTER)
    time.sleep(2)

    txt = browser.find_element_by_class_name("search-count").text
    if txt in ordesless:
        txt2 = ''
        return txt2
    else:
        url = browser.current_url
        print 'start page: ' ,  url

    url_qs.en_queue(url)
    index  = 0
    while not url_qs.is_empty() :
            if index >= 3:
                break
            listret = read_one_page(url_qs)
            storelist = storelist + listret
            
            index = index +1 
    #print "store list: ....", storelist
    outstr = list2str(storelist)
    #print outstr
    return outstr

def read_one_page(url_qs):
    liststore = []
    if url_qs.is_empty() :
        return

    url = url_qs.de_queue()
    try:
        browser.get(url)
    except:
        return liststore
    
    time.sleep(2)
    try:
        details = browser.find_elements_by_class_name("//detail")
    except NoSuchElementException:
        details = None
        if details == None :
            return liststore
    
    for det in details:
        try :
            em = det.find_element_by_xpath(".//div[@class='util-clearfix address-chat']/span[@class='address util-clearfix']")
        except NoSuchElementException:
            em = None
        if em is None:
            return liststore
        try :
            hrefs= em.find_elements_by_xpath("a[@href]")
        except NoSuchElementException:
            hrefs = None
            
        if hrefs is None:
            return liststore
        
        if len(hrefs) > 1:
            store =  hrefs[1].get_attribute("href")  
            store_name = store[store.find('store')+6:]
            liststore.append(store_name)
    #print liststore
    
    #加入下一页
    try:
        tops =browser.find_elements_by_xpath(".//div[@class='col-main']")
    except NoSuchElementException:
        tops = None
        return liststore
    
    if len(tops)>0:
        top = tops[0]
        try :
            navis = top.find_elements_by_xpath(".//div[@id='main-wrap']/div[@id='pagination-bottom']/div[@class='ui-pagination-navi util-left']")
        except NoSuchElementException:
            navis = None
            
        if navis is None:
            return liststore
        
        if len(navis) >0:
            nav = navis[0]
            try :
                page = nav.find_element_by_xpath(".//a[@class='page-next ui-pagination-next']")
            except NoSuchElementException:
                page = None 
            if page is None:
                    return liststore
            
            nexturl =  page.get_attribute("href")
            #print 'next url: ', nexturl
            url_qs.en_queue(nexturl)
        else :
            print "can not find list page !!"
        
    return liststore


    
def readKeylist(filename):
    keylist = []
    keyfile = file(filename,'rb')
    reader = csv.reader(keyfile)
    for line in reader:
        string_eng = 1
        for ch in line[1]:
            if ch>'\x7f':
                string_eng = 0
                break;

        if string_eng ==1:
            data = (line[0], line[1],line[2],line[3],line[4],line[5], line[6], line[7], line[8])
            #data = (line[0], line[1], line[2])
            keylist.append(data)
    keyfile.close()
    return keylist

#main from here
keylist=[]
outlist=[]
keylist = readKeylist("needlongwords.csv")
browser = webdriver.Chrome()

index = 0
for key in keylist:
    print index
    keyword =  key[7]
    strout = readorder_ofkey(key)
    print strout

    data = (key[0], key[1], key[3],key[4],key[5], key[6], key[7], key[8], strout)
    outlist.append(data)
    index = index +1

    if index == 100:
         writelist('outlong_1.csv', outlist)
    if index == 200:
         writelist('outlong_2.csv', outlist)
    if index == 300:
         writelist('outlong_3.csv', outlist)
    if index == 300:
         writelist('outlong_4.csv', outlist)
    if index == 400:
         writelist('outlong_5.csv', outlist)
    if index == 600:
         writelist('outlong_6.csv', outlist)
    if index == 700:
         writelist('outlong_7.csv', outlist)
browser.quit()

writelist('out_long_all.csv', outlist)
print ".............task over .......check out : out_long_all.csv......."
        

