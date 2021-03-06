# -*- coding: cp936 -*-
import time
import codecs
import sys
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pywinauto
from ctypes import windll

from bs4 import BeautifulSoup

#不加如下行，无法打印Unicode字符，产生UnicodeEncodeError错误。?
#sys.stdout = codecs.lookup('iso8859-1')[-1](sys.stdout)

from lxml import *
import lxml.html
import urllib2
from urllib2 import Request, urlopen, URLError
import lxml.html as H
from lxml.html import fromstring, tostring
from lxml import etree

import sqlite3

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
        
def readkeyfile(path, savelist) :
    tfile = file(path,'rb')
    reader = csv.reader(tfile)
    for line in reader:
        string_eng = 1
        for ch in line[1]:
            if ch>'\x7f':
                string_eng = 0
                break;

    if string_eng ==1:
        data = (line[0],line[1])
        savelist.append(data)

    tfile.close()

#open browser, enter key
def read_newaddress(key):
    browser = webdriver.Chrome()
    browser.get("http://www.aliexpress.com")
    time.sleep(5)
    browser.find_element_by_class_name("search-key").clear()
    browser.find_element_by_class_name("search-key").send_keys(key)
    browser.find_element_by_class_name("search-key").send_keys(Keys.ENTER)
    time.sleep(3)

    view = browser.find_element_by_id("view-filter")
    buts= view.find_elements_by_xpath(".//div[@class='narrow-down-bg']")
    new = buts[2]
    newurl = new.find_element_by_xpath(".//a[@href]")
    print newurl.get_attribute("href")
                                      
    time.sleep(2)
    
    #获取地址
    address = browser.current_url
    print address
    browser.close()

    #根据地址遍历找新产品
    addressnew = address
    #+ "&site=glo&groupsort=1&SortType=create_desc&shipCountry=all"
    return addressnew

def get_ordnumber(str):
    start = str.index('(')
    end =str.index(')')
    num = int(str[start+1:end])
    return num


def find_have_order(doc, order_list):
    url = ""
    price =""
    orderstr =""
    page=""

    time.sleep(1)
    
    #记录当前页码
    pages = doc.xpath("//span[@class='ui-pagination-active']")
    if len(pages) > 0:
        page = pages[0].text
    print ".........................now page: ", page

    #获取订单数 > 0的产品
    infos = doc.xpath("//div[@class='info infoprice']")
    for info in infos:
        orders = info.xpath(".//div[@class='rate-history']/span[@class='order-num']")
        for order in orders:
            nullorders = 0
            str = tostring(order)
            if  "Orders  (0)" in str:
                nullorders = nullorders +1
            else:
                start = str.index("Orders")
                end = str.index("</em")
                orders = str[start+8:end]

                start = str.index("http:")
                end = str.index("#thf")
                #urls = order.xpath(".//a[@class='order-num-a']/@href")
                url = str[start:end]

                prices = info.xpath(".//span[@class='price price-m']/span[@class='value']")
                price = prices[0].text

                ordnum = get_ordnumber(orders)
                print "order number : ", ordnum
                data = [ url, price,  page, "dress", "1", ordnum]
                order_list.append(data)
                
        #read order info
        
                
def find_urls(url, url_qs, order_list):
    if url ==  None:
        return

    timeout = 1

    try:
        response = urllib2.urlopen(url)
        time.sleep(2)
        f=response.read()
        time.sleep(2)
        doc = H.document_fromstring(f)
        time.sleep(1)
        #查找定单数>0
       
        find_have_order(doc,order_list)
        
        #查找下一页
        tops =doc.xpath(".//div[@class='col-main']")
        if len(tops)>0:
            top = tops[0]
            navis = top.xpath(".//div[@id='main-wrap']/div[@id='pagination-bottom']/div[@class='ui-pagination-navi util-left']")
            if len(navis) >0:
                nav = navis[0]
                pages = nav.xpath(".//a[@class='page-next ui-pagination-next']/@href")
                if len(pages) ==0 :
                    return 
                num =0
                for pg in pages:
                   url_qs.en_queue(pg)
                   num = num +1 
        else :
            print "can not find list page !!"
        
        
    except IOError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        else:
            print 'Failed to open url, not found reason'



    
def getNewList(url,key):
    url_qs = Queue()
    url_qs.en_queue(url)
    order_list = []
    
 
    while not url_qs.is_empty() :
  
       url =  url_qs.de_queue()
       find_urls(url, url_qs, order_list)
       



#     读取要扫描的类别和关键词
new_list = []
key_list=[]
key_list = ["crop top", "floral playsuit"]
#    开始扫描类别新目标
for key in key_list:
    print key
    newaddress = read_newaddress(key)
    ret = getNewList(newaddress, key)



