# coding = utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv


keylist = []
outlist = []
keyfile = file('searchkey1.csv','rb')
reader = csv.reader(keyfile)
for line in reader:
    string_eng = 1
    for ch in line[1]:
        if ch>'\x7f':
            string_eng = 0
            break;

    if string_eng ==1:
        #data = (line[0], line[1], line[3],line[4],line[5], line[6], line[7], line[8])
        data = (line[0], line[1], line[3],line[4],line[5], line[6])
        keylist.append(data)

keyfile.close()

print "keyword numbers :"
print len(keylist)
#for key in keylist:
#    print key
print "......................read key word ok................."


browser = webdriver.Chrome()
#browser = webdriver.Firefox()

browser.get("http://www.aliexpress.com")
time.sleep(5)

index =0
for key in keylist:
    print index
    index = index+1
    try :
        elem = browser.find_element_by_class_name("search-key")
    except Exception,e:
        print e
        
    elem.clear()
    elem.send_keys(key[1])
    elem.send_keys(Keys.ENTER)
    time.sleep(6)
    try :
        elem2 = browser.find_element_by_class_name("search-count")
        txt = elem2.text
    except Exception,e:
        print e
        print "Can not open the url ..........."
        browser.get("http://www.aliexpress.com")
        time.sleep(5)

        browser.find_element_by_class_name("search-key").clear()
        browser.find_element_by_class_name("search-key").send_keys(key[1])
        browser.find_element_by_class_name("search-key").send_keys(Keys.ENTER)
        time.sleep(6)
        try :
            txt = browser.find_element_by_class_name("search-count").text
        except Exception,e:
            txt = ' '
        
    #data = (key[0],key[1],key[2],key[3], key[4], key[5], key[6], key[7],txt)
    data = (key[0],key[1],key[2],key[3], key[4], key[5],txt)
    outlist.append(data)
    #print data
    time.sleep(2)
browser.quit()

print "check words:"
print len(outlist)
print ".....................check key word ok................."
    
outfile = file('out_search1.csv','wb')
writer = csv.writer(outfile)
for data in outlist:
    writer.writerow(data)
outfile.close()


print ".....................task over , please check out file: out_search.csv ................."

