
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import csv




def readorders1(browser):

    orderstr =''
    try :
        elem = browser.find_element_by_id('hs-list-items')
    except NoSuchElementException:
        elem = None
    if elem is not None:
        itemlist = elem.find_elements_by_xpath(".//li")
        print len(itemlist)

   
        for item in itemlist:
            try :
                info1 = item.find_element_by_xpath(".//div[@class='info infoprice']")
            except NoSuchElementException:
                info1 = None
                return ''
            try :
                info2 = info1.find_element_by_xpath(".//div[@class='rate-history']/span[@class='order-num']")
            except NoSuchElementException:
                info2 = None
                return ''
            try:
                ords = info2.find_element_by_css_selector("a em").text
            except NoSuchElementException:
                orderstr = ''
                return ''         
            orderstr += ords[ords.find('('):]
            
    return orderstr

           
def readorders2(browser):
    orderstr =''
    try :
        elem = browser.find_element_by_id('hs-below-list-items')
    except NoSuchElementException:
        elem = None
    if elem is not None:
        itemlist = elem.find_elements_by_xpath(".//div[1]/ul[1]/li")
        #print len(itemlist)

        for item in itemlist:
            try :
                info1 = item.find_element_by_xpath(".//div[@class='info infoprice']")
            except NoSuchElementException:
                info1 = None
                return ''
            try :
                info2 = info1.find_element_by_xpath(".//div[@class='rate-history']/span[@class='order-num']")
            except NoSuchElementException:
                info2 = None
                return ''
            try:
                ords = info2.find_element_by_css_selector("a em").text
            except NoSuchElementException:
                orderstr = ''
                return  ''          
            orderstr += ords[ords.find('('):]
           
    return orderstr

def writelist(filename, outlist):
    outfile = file(filename,'wb')
    writer = csv.writer(outfile)
    for data in outlist:
        orders = data[3];
        count = orders.count('(0)')
        if count > 5 :
            continue
        writer.writerow(data)
    outfile.close()

            
keylist = []
outlist = []
ordesless =['0', '1', '2', '3']
keyfile = file('searchorderkey.csv','rb')
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
    browser.find_element_by_class_name("search-key").clear()
    browser.find_element_by_class_name("search-key").send_keys(key[7])
    browser.find_element_by_class_name("search-key").send_keys(Keys.ENTER)
    time.sleep(6)
    
    txt = browser.find_element_by_class_name("search-count").text
    if txt in ordesless:
        txt2 = ''
        data = (key[0], key[1], key[3],key[4],key[5], key[6], key[7], key[8], txt, txt2)
        #data = (key[0],key[1],key[2],txt,txt2)
        outlist.append(data)
        time.sleep(3)
    else:
        str1=''
        str2=''
        str1 = readorders1(browser)
        str2 = readorders2(browser)
        txt2 = str1+str2

        data = (key[0], key[1], key[3],key[4],key[5], key[6], key[7], key[8], txt, txt2)
        #data = (key[0],key[1],key[2],txt,txt2)
        outlist.append(data)
        time.sleep(1)
        
    #print data   

   
    if index == 200:
         writelist('outorder_2.csv', outlist)

    if index == 400:
         writelist('outorder_4.csv', outlist)

    if index == 600:
         writelist('outorder_6.csv', outlist)
         
    if index == 800:
         writelist('outorder_8.csv', outlist)

    if index == 1000:
         writelist('outorder_10.csv', outlist)

    if index == 1200:
         writelist('outorder_12.csv', outlist)

    if index == 1500:
         writelist('outorder_15.csv', outlist)
        
browser.quit()

print "check words:"
print len(outlist)
print ".....................check key word ok................."
writelist('outorder_all.csv', outlist)

print ".....................task over , please check out file: outorder_all.csv ................."


            
        
    
