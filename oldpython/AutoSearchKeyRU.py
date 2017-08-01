# coding = utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

def sendtoout(outlist, filename):
    outfile = file(filename,'wb')
    writer = csv.writer(outfile)
    for data in outlist:
        writer.writerow(data)

    outfile.close()

keylist = []
outlist = []
keyfile = file('searchkey_ru.csv','rb')
reader = csv.reader(keyfile)
for line in reader:
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

browser.get("http://ru.aliexpress.com")
time.sleep(5)

index =0

for key in keylist:
    print index
    index = index+1
    browser.find_element_by_class_name("search-key").clear()
    browser.find_element_by_class_name("search-key").send_keys(key[1].decode("gb2312"))
    browser.find_element_by_class_name("search-key").send_keys(Keys.ENTER)
    time.sleep(6)
    
    txt = browser.find_element_by_class_name("search-count").text
    
    #data = (key[0],key[1],key[2],key[3], key[4], key[5], key[6], key[7],txt)
    data = (key[0],key[1],key[2],key[3], key[4], key[5],txt)
    outlist.append(data)
    time.sleep(2)

    if index == 100:
        sendtoout(outlist,'outsearch_1.csv')
    if index == 200:
        sendtoout(outlist,'outsearch_2.csv')
    if index == 300:
        sendtoout(outlist,'outsearch_3.csv')
    if index == 400:
        sendtoout(outlist,'outsearch_4.csv')
 
browser.quit()

print "check words:"
print len(outlist)
print ".....................check key word ok................."

outfile = file('out_search1_ru.csv','wb')
writer = csv.writer(outfile)
for data in outlist:
    writer.writerow(data)
outfile.close()


print ".....................task over , please check out file: out_search.csv ................."

