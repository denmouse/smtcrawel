#-----------------------------
##### Ali_2ndKey.py
#### by deng.hp 2015
### needkeysecond.csv from aliexpress
#-------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import csv


def sendtoout(outlist, filename):
    outfile = file(filename,'wb')
    writer = csv.writer(outfile)
    for data in outlist:
        writer.writerow(data)

    outfile.close()



#1. read the keywords list
keylist = []
outlist = []
keyfile = file('needkeysecond.csv','rb')
reader = csv.reader(keyfile)
for line in reader:
    string_eng = 1
    for ch in line[1]:
        if ch>'\x7f':
            string_eng = 0
            break;

    if string_eng ==1:
        data = (line[0], line[1], line[2], line[3],line[4],line[5], line[6])
        keylist.append(data)

keyfile.close()

print "keyword numbers :", len(keylist)
print "......................read key word ok................."


#2. open chrome 
browser = webdriver.Chrome()
browser.get("http://www.aliexpress.com")
time.sleep(5)

#3. for every keyword in list,find second key
index =0
for key in keylist:
    print index
   
    browser.find_element_by_class_name("search-key").clear()
    browser.find_element_by_class_name("search-key").send_keys(key[1])
    
    time.sleep(5)

    elem = browser.find_element_by_class_name("ui-autocomplete-ctn ")
    elem2list = elem.find_elements_by_xpath(".//li")
  
    for elem2item in elem2list:
        try:
            txt1 = elem2item.get_attribute("data-value")
        except BadStatusLine:
            txt1 = ''
            
        try:
            elem3= elem2item.find_element_by_class_name("suggest-count")
        except NoSuchElementException:
            elem3=None

        if elem3 is not None:
            txt2 = elem3.find_element_by_xpath(".//span[@class='count-value']").text
            data = (key[0],key[1],key[2],key[3], key[4], key[5], key[6],txt1, txt2)
            outlist.append(data)
  
    if index == 200:
        sendtoout(outlist,'keysecond_2.csv')
  
    if index == 400:
        sendtoout(outlist,'keysecond_4.csv')

    if index == 600:
        sendtoout(outlist,'keysecond_6.csv')

    if index == 800:
        sendtoout(outlist,'keysecond_8.csv')

    if index == 1000:
        sendtoout(outlist,'keysecond_10.csv')

    if index == 1400:
        sendtoout(outlist,'keysecond_14.csv')
        
    if index == len(keylist)-1:
        sendtoout(outlist,'keysecond_all.csv')
    index = index+1           
 

#4. close browser
browser.quit()

print "check words:"
print index
print ".....................task over , please check out file ..."

