# -*- coding: gb2312 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pywinauto
from ctypes import windll


plist=[]
badvpnlist = [0,1,7,9,10,11,14,18,19,22,23,26,31,32,36,39,40,42]

try:
    f = open('E:/googledrive/products/product_list.txt', 'r')
    while 1:
        lines = f.readlines(1000)
        if not lines:
            break
        for line in lines:
            if len(line)>2:
                plist.append(line)
         
except IOError:
    print('Read products list file Error')
finally:
    f.close

print('read product numbers:')
print len(plist)


#open vpn 
app = pywinauto.application.Application()
app.start_(r"D:\vpn\51VPN_2013\51vpn")
time.sleep(2)

listview = app.Dialog.SysListView32
if listview==0:
    print('do not find the list ivew ')

#begin test , for all lines from 0 to 49 
for line in range(14, 49) :

    if line in badvpnlist:
        continue

   
    #click "disconnect"
    discon = app[ur'我要网络加速器2013 SP4'][ur'断开']
  #  discon = app.Dialog[ur'断开']
    if discon == 0 :
        ok_window = app.window_(title = r"51VPN SAY")
        dlg =ok_window.Window_(title = ur"确定")
        if dlg.Exists():
            dlg.Click()
            sleep(2)

        discon = app[ur'我要网络加速器2013 SP4'][ur'断开']
        if discon == 0:
            print "ERROR ::::::: disconnect button lost"
            break
    
    if discon.IsEnabled():
        discon.Click()
        time.sleep(10)
        print 'dicount .....'

    #select line
    listview = app[ur'我要网络加速器2013 SP4'].SysListView32
    if listview == 0:
        ok_con = app
    listview.Select(line)
    time.sleep(1)

    #click "connect "
    con = app.Dialog[ur'连接']
    if con == 0:
        print "ERROR ::::::: can not find connect button ..."
        break;
    
    if con.IsEnabled():
        con.Click()
        print "connect... to line :", line
        time.sleep(20)

    ok_window = app.window_(title = r"51VPN SAY")
    if ok_window ==0 :
        print "---------->ok window not found,can not connect to: ", line
        continue
    dlg =ok_window.Window_(title = ur"确定")
    if dlg.Exists():
        dlg.Click()
        
    dlgerr=app.window_(title = r"51vpn").Window_(title = ur"确定")
    if dlgerr.Exists():
         print "---------->can not connect to: ", line
         dlgerr.Click()
         continue;
    
    #app.window_(title = r"51VPN SAY").Window_(title = ur"确定").Click()
    #print "connect ok to  :", line
    #    

    #make sure connect ok!
    state=app.Dialog.Window_(title = ur'连接成功')
    times = 0
    while state == 0 :
        time.sleep(5)
        times = times + 1
        if times >10:
            break
    
    #begain web browser 
    for i in range(0, 5):
        browser = webdriver.Chrome()
    
        # browser all the products every one time in 500s
        for url in plist :
            browser.get(url)
            time.sleep(2)
            browser.find_element_by_id('page-detail').send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            browser.find_element_by_id('page-detail').send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            browser.find_element_by_id('page-detail').send_keys(Keys.PAGE_DOWN)
            browser.find_element_by_id('page-detail').send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

        time.sleep(2)
        print("TEST Over ........... , No: ")
        print(i)
        browser.quit()
        time.sleep(2)
print ("test is over ............................!!!!")


                              
