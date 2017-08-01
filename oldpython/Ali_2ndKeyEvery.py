#-----------------------------
##### Ali_2ndKey_everyday.py
#### by deng.hp 2015
### needkeysecond.csv from aliexpress
#-------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import csv

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
            data = (line[0],line[1], line[2])
            savelist.append(data)

    tfile.close()

def sendtoout(outlist, filename):
    outfile = file(filename,'wb')
    writer = csv.writer(outfile)
    for data in outlist:
        writer.writerow(data)

    outfile.close()

def destAdd(dest_list, keyword, number):
    index = len(dest_list)
    data = (index, keyword, number)
    dest_list.append(data)

def get_number(text_in):
    if text_in == '':
        return 0
    
    text_out = text_in.replace(',', "")
    number = int(text_out)
    return number

        
        
    
#in, out list: index, keyword, product num
def get2ndKey(in_list, out_list,dest_list, adddest):
    if adddest == False:
        index = len(dest_list)
    else:
        index = 0
        
    for key in in_list:
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
                
            if txt1 == key[1]: #list key againg below, ignore it 
                continue
            
            try:
                elem3= elem2item.find_element_by_class_name("suggest-count")
            except NoSuchElementException:
                elem3=None

            if elem3 is not None:
                txt2 = elem3.find_element_by_xpath(".//span[@class='count-value']").text
                data = (index, txt1, txt2)
                out_list.append(data)
                index = index+1
            
                # if number < 10000, add to dest list
                print data
                
                number = get_number(txt2)
                if number < 10000  and adddest == True:
                    destAdd(dest_list, txt1, txt2)
                    print 'add to dest'
            
 

#1. read the keywords list
key_list = []
readkeyfile('everyday_key.csv', key_list)

key2nd_list=[]
key3rd_list=[]
key4th_list=[]
outlist = []

#2. open chrome 
browser = webdriver.Chrome()
browser.get("http://www.aliexpress.com")
time.sleep(5)

#3. read 2nd key:
print key_list
print 'get start keywords ok ............................'
get2ndKey(key_list, key2nd_list, outlist, True)
print key2nd_list
print 'get second keywords ok ...........................'
get2ndKey(key2nd_list, key3rd_list,outlist, True)
print 'get third keywords ok ...........................'
sendtoout(key3rd_list, 'keyword3_today.csv')

#get2ndKey(key3rd_list, outlist, outlist, False)
#write out
#sendtoout(outlist, 'keyword_today.csv')
print 'get all keywords ok .............................'
#4. close browser
browser.quit()

print ".....................task over , please check out file ..."

