#coding:utf-8

import time
import codecs
import sys
import csv
import sys,os,re
#不加如下行，无法打印Unicode字符，产生UnicodeEncodeError错误。?
#sys.stdout = codecs.lookup('iso8859-1')[-1](sys.stdout)

from lxml import *
import lxml.html
import urllib2
from urllib2 import Request, urlopen, URLError
import lxml.html as H
from lxml.html import fromstring, tostring
import threading
import socket

work_dir = "e:\work\data"
productlist = []
outlist = []
os_lock = threading.RLock()
thread_list = []


def sendtoout(outlist, filename):
    outfile = file(filename,'wb')
    writer = csv.writer(outfile)
    for data in outlist:
        writer.writerow(data)

    outfile.close()
    
def readproduct(py,productlist):
    productfile = file(py,'rb')
    reader = csv.reader(productfile)
    for line in reader:
        data = (line[0], line[1]) # index, product url
        productlist.append(data)

    productfile.close()

    print "read products ok......product numbers :"
    print len(productlist)


   
def getAttrs(dl):
    if dl == '':
        return
    if dl.find('Brand Name') >0:
        return
    
    atr_name=''
    atr_val=''
    
    start = dl.find('<dt>')
    end = dl.find(':</dt>')
    st = dl.find('dd title=\"')
    se = dl.find('</dd')
    if start>=0 and end>=start+4:
        atr_name = dl[start+4:end]
    if st >=0 and se >= st+10:
        val = dl[st+10:se]
        vle = val.find('">')
        atr_val = val[0:vle]
    dat =(atr_name,atr_val)
    return dat
    
#down .../c21101/c21101_1.jpg
def PicDown(work_path, prod_id, index, url, thread_id):
    dir_path = work_path + "/" + prod_id

    os_lock.acquire()
    #create dir
    if os.access(dir_path,0):
        pass
    else:
        os.makedirs(dir_path)
    os_lock.release()
     
    path = dir_path+prod_id+'_'+index +'.jpg'
    print 'down path: ', path
    try:
        print "thread: ", thread_id, " down pic: ", index, " now.........."
        data = urlib.urlopen(url).read()
        with open(path, "wb") as f:
            f.write(data)
        f.close()
    except:
        print " download error ..........."
        return 
    
    

class CPicDown(threading.Thread): #The timer class is derived from the class threading.Thread 
    def __init__(self, id_num, interval,work_dir, prod_id, index, aimurl):
        threading.Thread.__init__(self)
        self.thread_num = id_num# thread's number
        self.interval = interval # this attribute doesn't mean anything now,but it's future is bright..
        self.work_dir = work_dir
        self.prod_id = prod_id
        self.pic_index = index
        self.url = aimurl
        # url list that thread seek in
        self.thread_stop = False
                # flag to control thread
                
    def run(self):
        while not self.thread_stop:
            PicDown(self.work_dir, self.prod_id, self.pic_index, self.url,self.thread_num)

            
    def stop(self):
        self.thread_stop = True

def downProd(prod_id, url):
    timeout=1
    attrs_list=[]
    img_list = []
    print 'down : ', prod_id , '   ', url
    try:
        #data = ''
        #req = urllib2.Request(url,data,headers)
        #response = urllib2.urlopen(req)
        socket.setdefaulttimeout(10)
        req = urllib2.Request(url)
        #req.add_header('User-Agent' ,'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
        req.add_header('User-Agent', 'fake-client')
        response = urllib2.urlopen(req)
        
        f=response.read()
        print f
        doc = H.document_fromstring(f)
        try:
            dls =doc.xpath("//div[@id='product-desc']/div[1]/div/dl[@class='ui-attr-list util-clearfix']")
            for dl in dls:
                atr_dat = getAttrs(tostring(dl))
                attrs_list.append(atr_dat)

            print attrs_list
           
        except :
            spantxt=' '

        #all pics
        divs = doc.xpath("//div[@id='custom-description']/div[@class='ui-box-body']")
        for div in divs:
            print tostring(div)

        print 'img list len: ', len(img_list)
        print img_list
        print 'prod id:', prod_id, 'work dir:', work_dir
        #down pics:
        for i in range(len(img_list)):
            thread = CPicDown(i, 1, work_dir, prod_id, i, img_list[i])
            thread_list.append(thread)
            
        
    except IOError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        else:
            print 'Failed to open url, not found reason'
            
        
#main
readproduct("need_newprod.csv", productlist)
index=0
for elems in productlist:
    downProd(elems[0], elems[1])
    time.sleep(1)
   
