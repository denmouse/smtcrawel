# -*- coding: cp936 -*-
import time
import csv


#��ȡ�������ţ����������Ʒ�б����ң� ����������ʱ�䣬���ٺ�
#���򣬰���Ʒ������������ң�����һ���ܶ�
#���ɶ������ٱ�


def readorders(filename, orderlist):
    orderfile = file(filename,'rb')
    reader = csv.reader(orderfile)
    for line in reader:
        #�����ţ�״̬����������µ�ʱ�䣬����ʱ�䣬��������Ʒ�����ң����ٺ�,����ʱ��
        data = (line[0], line[1], line[3], line[5], line[6], line[9],line[11], line[15],line[24],line[25]) 
        if line[0] != "������":
            orderlist.append(data)

    orderfile.close()

def sumorders(orderlist):
    sum_orders=0
    sum_paid=0
    sum_unpaid=0
    sum_money =0
    
    sum_orders = len(orderlist)
    for ord in orderlist:
        if ord[4] =="" :
            sum_unpaid += 1
        else :
            sum_paid += 1
            sum_money += float(ord[5][1:len(ord[5])])
    print "   �ܶ�����ͳ��  "
    print "�ܶ�����", sum_orders, "      �ܽ��", sum_money
    print "��֧����",sum_paid
    print "δ֧��:", sum_unpaid
    print "δ֧���ʣ�", sum_unpaid/sum_orders
    
def country_sum(orderlist):
    list_country = {}
    for ord in orderlist :
        key = ord[7]
        if list_country.has_key(key):
            list_country[key] = list_country[key] +1
        else :
            list_country[key] = 1

    return list_country

def find_day(day, listday) :
    for index in range(len(listday)):
        data = listday[index]
        if day == data[0] :
            return index
    return -1

def day_sum(orderlist):
    list_day = []
    for ord in orderlist:
        day =  ord[3][0:10]
        index = find_day(day, list_day)

        if index == -1 :
            data = (day, 1)
            list_day.append(data)
        else:
            val = list_day[index][1] + 1
            data = (day, val)
            list_day[index] = data
    list_day.sort()
    return list_day

def get_code(str):
    #(�̼ұ���:J21101_1__L)
    strhead = "(�̼ұ���:"
    index = str.find(strhead)
    if index < 0 :
        return ""
    ind_start = str.find(strhead)
 
    code = str[ind_start + 10: ind_start + 21]
    return code

def get_count(str):
 
    ss = []
    ss = str.split(":")
   
    ind = ss[1].find("piece")
    cnt = int(ss[1][0:ind])
    return cnt

def calc_attr(strattrib) :
    in_attr = 0
    in_code = 0
    in_count = 0
    
    in_attr = strattrib.find("(��Ʒ����")
    in_code = strattrib.find("(�̼ұ���")
    in_count = strattrib.find("(��Ʒ����")
    
    if in_attr + in_code + in_count <=0 :
        return 
    
    count = 0
    if in_attr > 0 and in_count >0 :
        listattr = strattrib.split("\n")
        if in_code < 0 :
            code = "000000_0__0"
            count = get_count(listattr[2])
        else :
            code = get_code(listattr[2])
            count = get_count(listattr[3])
    data = (code , count)
    return data

def sortedDictValues(adict): 
    items = adict.items() 
    items.sort() 
    return [value for key, value in items] 
        
def prod_sum(orderlist):
    str_list = []
    prod_list = []
    sum_list = {}
    for ord in orderlist:
        prods = ord[6]
        str_list = prods.split("��")
        if len(str_list) < 2 :
            return

        for prod_str in str_list:
            data = calc_attr(prod_str)
            prod_list.append(data)
       
    for  prod in prod_list:
        if prod is None:
            continue 
        code = prod[0]
        cnt = prod[1]
        if sum_list.has_key(code):
            sum_list[code] = sum_list[code] + cnt
        else :
            dat = (code, cnt)
            sum_list[code] = cnt

    return sum_list
 

        
orderlist = []
countrylist = []
prodlist =[]

#��ȡ����
readorders("test_sum.csv", orderlist)
#ͳ�Ʋ�Ʒ��������δ������
sumorders(orderlist)
#ͳ�ƹ���
countrylist = country_sum(orderlist)

#ͳ��ÿ����
daylist = day_sum(orderlist)

#ͳ�Ʋ�Ʒ��
sum_list = prod_sum(orderlist)

print "    ����ͳ��    "
for key in countrylist.keys():
    print key, countrylist[key]

print "    ����ͳ��   "
for day in daylist :
    print day

print "   ����Ʒ����  "
#value sorted
#dict= sorted(sum_list.iteritems(), key=lambda d:d[1], reverse = True)
#key sorted
out_sum= sorted(sum_list.iteritems(), key=lambda d:d[0]) 
for s in out_sum:
    print s[0], s[1]
   



