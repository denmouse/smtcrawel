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


def read_one_page(url_qs):

    liststore = []
    if url_qs.is_empty() :
        return
    url = url_qs.de_queue()
    print 'now url:',  url
    if url ==  None:
        return
    outlist = []
    
    timeout=1
    try:
        urs = str(url)
        response = urllib2.urlopen(urs.encode('utf-8'))

        time.sleep(2)
        f=response.read()
        time.sleep(2)
        doc = H.document_fromstring(f)
        time.sleep(1)

        #当前页
        pages = doc.xpath("//span[@class='ui-pagination-active']")
        if len(pages) > 0:
            page = pages[0].text
            print ".........................now page: ", page

            
        #读取每一页
        dots = doc.xpath(".//div[@class='address util-clearfix']")
        if len(dots)>0:
            for dt in dots:
                store = dt.xpath(".//a/@href")
                print store
                store_name = store[store.find('store')+6:]
                liststore.append(store_name)
        else:
            print 'dots len ', len(dots)
            return liststore
                

        

        #查找下一页
        tops =doc.xpath(".//div[@class='col-main']")
        if len(tops)>0:
            top = tops[0]
            navis = top.xpath(".//div[@id='main-wrap']/div[@id='pagination-bottom']/div[@class='ui-pagination-navi util-left']")
            if len(navis) >0:
                nav = navis[0]
                pages = nav.xpath(".//a[@class='page-next ui-pagination-next']/@href")
                if len(pages) ==0 :
                    print ' next pages is 0 '
                    return 
                for pg in pages:
                   url_qs.en_queue(pg)
        else :
            print "can not find list page !!"
            return storelist
        
        
    except urllib2.HTTPError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        else:
            print 'Failed to open url, not found reason'

    return liststore


def readorder_ofkey(key):
    ordesless =['0', '1', '2', '3']
    
    url_qs = Queue()
    
    storelist = []
    outstr = ''
    
    if browser is None:
        print "browser is not open!"
        return
    
    time.sleep(1)

    keyword = key[7]
    browser.find_element_by_class_name("search-key").clear()
    browser.find_element_by_class_name("search-key").send_keys(keyword)
    browser.find_element_by_class_name("search-key").send_keys(Keys.ENTER)
    time.sleep(1)

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
browser.get("http://www.aliexpress.com")


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
        


            
        
    
