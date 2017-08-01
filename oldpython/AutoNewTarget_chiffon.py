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

database_name='target_chiffon.db'

#���������У��޷���ӡUnicode�ַ�������UnicodeEncodeError����?
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
    
    #��ȡ��ַ
    address = browser.current_url
    print address
    browser.close()

    #���ݵ�ַ�������²�Ʒ
    addressnew = address + "&site=glo&groupsort=1&SortType=create_desc&shipCountry=all"
    return addressnew

def read_newaddress_cat(key):
    browser = webdriver.Chrome()
    browser.get("http://www.aliexpress.com")
    time.sleep(5)
    browser.find_element_by_class_name("search-key").clear()
    browser.find_element_by_class_name("search-key").send_keys(key)
    browser.find_element_by_class_name("search-key").send_keys(Keys.ENTER)
    time.sleep(3)

    view = browser.find_element_by_class_name("view-more")
    #newurl = view.find_element_by_xpath(".//a[@href]")
    addr = view.get_attribute("href")
                                      
    time.sleep(2)
    
    #��ȡ��ַ�б���ַ
    print addr
    browser.get(addr)
    time.sleep(2)
    
    view = browser.find_element_by_id("view-filter")
    butn= view.find_element_by_xpath(".//span[@class='view-btn']")
    new = butn
    newurls = new.find_elements_by_xpath(".//a[@href]")
    addr =  newurls[1].get_attribute("href")

    #��ȡ�б�����new list��ַ
    print addr
    browser.get(addr)
    time.sleep(2)
    view = browser.find_element_by_id("view-filter")
    buts= view.find_elements_by_xpath(".//div[@class='narrow-down-bg']")
    new = buts[2]
    newurl = new.find_element_by_xpath(".//a[@href]")

    addr = newurl.get_attribute("href")
    print addr
    
    browser.close()
    return addr


def get_number_txt(strin):
    ordernum = '0'
    start = strin.find("Total Orders")
    end = strin.find("</em>")
    if start >=0 and end >=start+13:
        #print "stand in: ", start, end 
        orders = strin[start+13:end]
        #print "ordr is: ", orders
        ordernum = get_ordnumber(orders)
        #print "order", ordernum
    return ordernum

def get_link_txt(strin):
    link = ''
    start = strin.find("href")
    end = strin.find("#th")
    if start >=0 and end >= start+6:
        link = strin[start+6:end]
        #print "link is: ", link
    return link

def get_price_txt(strin):
    price = 'USD 0'
    #print strin
    start = strin.find("itemprop=\"price")
    end =strin.find("</span>")
    #print "price index:", start, end
    if start >=0 and end >= start+17:
        price = strin[start+17:end]
        #print "price is :", price
    return price

def get_order_info(strs):
    
    lstorder = []
    if strs is None:
        return None
    if strs =='':
        return None
    lstproducts = []
    
    lstproducts = strs.split("price price-m")
    
    for ls in lstproducts:
           orderst = ls.find("order-num-a ")
           orderen = ls.find("class=\"add-to-wishlis\">")
           stt = ls[orderst:orderen]
           if "Orders  (0)" in stt:
               continue
           ordernum = get_number_txt(stt)
           link = get_link_txt(stt)

           orderst = ls.find("price price-m")
           orderen = ls.find("rate-history")
           stt = ls[orderst:orderen]
           price = get_price_txt(stt)
           
           #print "link, ordrnum , price", link, ordernum,price
           data = (link, ordernum, price)
           lstorder.append(data)
           
    return lstorder
    
def get_ordnumber(str):
    start = str.index('(')
    end =str.index(')')
    num = int(str[start+1:end])
    return num

def getupdateorders(url):
    if len(url)< 20 :
        return 0
    timeout=1
    try:
        response = urllib2.urlopen(url)
        time.sleep(1)
        f=response.read()
        doc = H.document_fromstring(f)
        try:
            spans=doc.xpath(".//div[@class='detail-page']/div[@id='base']/div[1]/div/div[1]/span[@class='orders-count']")
            spantxt=tostring(spans[0])
            str1='<b>'
            str2='</b>'
            ins=spantxt.find(str1)+3
            ine= spantxt.find(str2)
            if ins >=0 and ine > ins:
                orders=spantxt[ins : ine]
                num = int(orders)
                
            else:
                num = 0
                print 'not found orders'
                
        except :
            spantxt=' '
            num = 0
        return num;
        
    except IOError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        else:
            print 'Failed to open url, not found reason'

def find_have_order(doc, order_list):
    url = ""
    price =""
    orderstr =""
    page=""
    
    #��¼��ǰҳ��
    pages = doc.xpath("//span[@class='ui-pagination-active']")
    if len(pages) > 0:
        page = pages[0].text
    print ".........................now page: ", page

    #��ȡ������ > 0�Ĳ�Ʒ
    infos = doc.xpath("//div[@class='info infoprice']")
    for info in infos:
        orders = info.xpath(".//div[@class='rate-history']/span[@class='order-num']")
        for order in orders:
            nullorders = 0
            str = tostring(order)
            if  "Orders  (0)" in str:
                nullorders = nullorders +1
            else:
                
                if "Orders " in str:
                    start = str.index("Orders")
                    end = str.index("</em")
                    orders = str[start+8:end]
                else:
                    if "Order " in str:
                        start = str.index("Order")
                        end = str.index("</em")
                        orders = str[start+8:end]
                

                start = str.index("http:")
                end = str.index("#thf")
                #urls = order.xpath(".//a[@class='order-num-a']/@href")
                url = str[start:end]
                print "new product--->", url, "  ", orders
                
                prices = info.xpath(".//span[@class='price price-m']/span[@class='value']")
                price = prices[0].text
                
                ordnum = get_ordnumber(orders)
                data = [ url, price,  page, "dress", "1", ordnum]
                order_list.append(data)


    #�°벿
    try:
        downlst = []
        top = doc.xpath(".//div[@id='hs-below-list-items']")
        if len(top) > 0 :
            tp = top[0].xpath(".//script")
            strout = tostring(tp[0])
            downlst = get_order_info(strout) #url, price, page,  ordnum
            for data in downlst:
                link = data[0]
                order = data[1]
                price = data[2]
                newdata = (link, price,page,"dress", "1", order)
                order_list.append(newdata)
        
            
        #read order info
    except IOError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
                
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
        #���Ҷ�����>0
       
        find_have_order(doc,order_list)
        
        #������һҳ
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
       
    
    #order_listд�����ݿ�
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    
    for ord in order_list:
        addr = ord[0]
        pri = ord[1]
        pag = ord[2]
        k = key
        rec = 1
        ord0 = ord[5]

        cur.execute("INSERT INTO tab_dress (address, price, page, keyword, record , order0) VALUES(?, ?, ?, ?, ?,?)",( addr, pri,pag, k, rec, ord0) )
    con.commit()
    con.close()
    
#���¶�������
def updateorders(con, cur):
    oldlist = []
    cur.execute('SELECT * FROM tab_dress where record=1 and order0<10')
    out = cur.fetchall()
    if len(out)<=0 :
        print " NO Record in this databas!!"
    else :
        print " get record : ",len(out)
        for line in out:
            oldlist.append(line)
    #data 0 id, data1 url, data2 record,
    index = 0
    for data in oldlist:
        # ��ȡ�µ�orders
        print data[0], " : ", data[1]
        new_orders =  getupdateorders(data[1])
        if new_orders is "":
            continue
        if new_orders is None:
            continue
       
        print "get orders", int(new_orders)
        if data[5] == 0 :
            sql = "update tab_dress set record=:rec, order0=:val1 where dressid="+ str(data[0])
            cur.execute( sql, {"rec":1, "val1":int(new_orders)})
            
        if data[5] == 1 :
            sql = "update tab_dress set record=:rec, order1=:val1 where dressid="+ str(data[0])
            cur.execute( sql, {"rec":2, "val1":int(new_orders)})
            print sql
        if data[5] == 2 :
            sql = "update tab_dress set record=:rec, order2=:val1 where dressid="+ str(data[0])
            cur.execute( sql, {"rec":3, "val1":int(new_orders)})
     
        if data[5] == 3 :
            sql = "update tab_dress set record=:rec, order3=:val1 where dressid="+ str(data[0])
            cur.execute( sql, {"rec":4, "val1":int(new_orders)})
        
        if data[5] == 4 :
            sql = "update tab_dress set order4=:val1 where dressid="+ str(data[0])
            cur.execute( sql, {"val1":int(new_orders)})

        index = index +1
        if index%100 ==0 :
             con.commit()
    con.commit()
    

#1. �����ݿ�
    
con = sqlite3.connect(database_name)
cur = con.cursor()
cur.execute('SELECT * FROM tab_dress')
#print cur.fetchall()

#2. ���¶�������
updateorders(con, cur)
con.close()

#3. ɨ���µ�Ŀ��
#     ��ȡҪɨ������͹ؼ���
new_list = []
key_list=[]
##readkeyfile('target_key.csv',key_list)

#addr = "http://www.aliexpress.com/category/200003482/dresses.html?site=glo&SortType=create_desc&shipCountry=us"
#ret = getNewList(addr, "dress")

key_list = ["chiffon dress"]
#key_list = ["beach dresses","sleeveless dresses", "summer dresses", "mini dresses", "casual dresses", "chiffon dresses"]
for key in key_list:
    print key
    newaddress = read_newaddress(key)
    print "now address: ", newaddress
    ret = getNewList(newaddress, key)
    

#key_list = ["crop top"]
#    ��ʼɨ�������Ŀ��
#for key in key_list:
#    print key
#    newaddress = read_newaddress_cat(key)
#    print "now address: ", newaddress
#    ret = getNewList(newaddress, key)


