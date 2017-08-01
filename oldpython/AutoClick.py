# -*- coding: gb2312 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import pywinauto
from ctypes import windll


def readkeys(filename, keylist):
    keyfile = file(filename,'rb')
    reader = csv.reader(keyfile)
    for line in reader:
        data = (line[0], line[1], line[2], line[3])
        keylist.append(data)

    print "keyword numbers :"
    print len(keylist)
    keyfile.close()

def click1(index, browser, storename):
    try :
        elem = browser.find_element_by_id('hs-list-items')
    except NoSuchElementException:
        elem = None
    if elem is not None:
        itemlist = elem.find_elements_by_xpath(".//li")
        print len(itemlist)

        for item in itemlist:
            store = item.find_element_by_xpath(".//div[@class='detail']")
            store2 = store.find_element_by_xpath(".//div[@class='util-clearfix address-chat']/span[@class='address util-clearfix']")
            name =  store2.find_element_by_css_selector('a[title][href]').text

            if cmp(name,storename) ==0:
                item.find_element_by_xpath(".//div[@class='img']").click()
                print " clicked the product --->", index
                break
        
 
def click2(index,browser, storename):
    try :
         elem = browser.find_element_by_id('hs-below-list-items')
    except NoSuchElementException:
        elem = None
    if elem is not None:
        itemlist = elem.find_elements_by_xpath(".//div[1]/ul[1]/li")
        #print len(itemlist)

        for item in itemlist:
            store = item.find_element_by_xpath(".//div[@class='detail']")
            store2 = store.find_element_by_xpath(".//div[@class='util-clearfix address-chat']/span[@class='address util-clearfix']")
            name =  store2.find_element_by_css_selector('a[title][href]').text

            if cmp(name,storename) ==0:
                item.find_element_by_xpath(".//div[@class='img']").click()
                time.sleep(5)
                print " clicked the product --->", index
                break
        
 
def autoclick(file,times):
    # read keyword list 
    keylist = []
    outlist = []
    clicklist = []
    readkeys(file,keylist)

    #open browser
    browser = webdriver.Chrome()
    browser.get("http://www.aliexpress.com")
    time.sleep(5)
    
    #init 
    for i in range(0, len(keylist)):
        data = (0, 0)
        clicklist.append(data)
    
    #click for many times
    for times in range(0, times):
        index =0
        for key in keylist:
            print index, key[1], key[2]
            page = key[2]
        
            browser.find_element_by_class_name("search-key").clear()
            browser.find_element_by_class_name("search-key").send_keys(key[1])
            browser.find_element_by_class_name("search-key").send_keys(Keys.ENTER)
            time.sleep(3)

        #go to page:
            if page > 1:
                pagenum = browser.find_element_by_id("pagination-bottom-input")
                pagenum.send_keys(key[2])
                pagenum.send_keys(Keys.ENTER)
                time.sleep(5)
            time.sleep(2)
            click1(index,browser, key[3])
            click2(index,browser, key[3])
           
            time.sleep(2)
            index = index+1
        
    browser.quit()
    print ".....................click task over "

def openvpn(app, line):
    listview = app.Dialog.SysListView32
    if listview==0:
        print('do not find the list ivew ')

    #click "disconnect"
    discon = app[ur'我要网络加速器2013 SP4'][ur'断开']
    if discon == 0 :
       if find_con_ok(app) == True :
           discon = app[ur'我要网络加速器2013 SP4'][ur'断开']
       else :
           print 'ERROR :::::::can not find disconnect button '
        
    if discon.IsEnabled():
        discon.Click()
        time.sleep(10)
        print 'dicount .....'

    #select line
    listview = app[ur'我要网络加速器2013 SP4'].SysListView32
    if listview == 0:
        if find_con_ok(app) == True :
            listview.Select(line)
            time.sleep(1)
        else:
            print "ERROR ::::::: can not find list view "
            

    #click "connect "
    con = app.Dialog[ur'连接']
    if con == 0:
        if find_con_ok(app) == True :
            listview.Select(line)
            time.sleep(1)
        else:
            print "ERROR ::::::: can not find connect button ..."
    
    if con.IsEnabled():
        con.Click()
        print "connect... to line :", line
        time.sleep(20)

    #make sure the connection 
    ok_window = app.window_(title = r"51VPN SAY")
    if ok_window ==0 :
        print "---------->ok window not found,can not connect to: "
        print line
    dlg =ok_window.Window_(title = ur"确定")
    if dlg.Exists():
        dlg.Click()
        
    dlgerr=app.window_(title = r"51vpn").Window_(title = ur"确定")
    if dlgerr.Exists():
         print "---------->can not connect to: ", line
         dlgerr.Click()
    
    #app.window_(title = r"51VPN SAY").Window_(title = ur"确定").Click()
    #print "connect ok to  :", line
    #    

    #make sure connect ok!
    state=app.Dialog.Window_(title = ur'连接成功')
    times = 0
    while state == 0 :
        
        time.sleep(5)
        times = times + 1
        if times >5:
            break
        state=app.Dialog.Window_(title = ur'连接成功')


 #open vpn
badvpnlist = [0,1,3,7,11,13,16,18,28,29,30,39,42,43,44,45,52,53,]
app = pywinauto.application.Application()
app.start_(r"D:\vpn\51VPN_2013\51vpn")
time.sleep(2)

for line in range(19, 51) :
    if line in badvpnlist:
        continue
    openvpn(app, line)
    autoclick('products.csv',1)
    
