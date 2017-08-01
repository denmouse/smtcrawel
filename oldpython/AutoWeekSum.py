# -*- coding: cp936 -*-
import time
import csv


#读取，订单号，买家名，产品列表，国家， 订单金额，付款时间，跟踪号
#排序，按产品，按付款，按国家，按周一，周二
#生成订单跟踪表


def readorders(filename, orderlist):
    orderfile = file(filename,'rb')
    reader = csv.reader(orderfile)
    for line in reader:
        #订单号，状态，买家名，下单时间，付款时间，订单金额，产品表，国家，跟踪号,发货时间
        data = (line[0], line[1], line[3], line[5], line[6], line[9],line[11], line[15],line[24],line[25]) 
        if line[0] != "订单号":
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
    print "   总订单数统计  "
    print "总订单：", sum_orders, "      总金额", sum_money
    print "已支付：",sum_paid
    print "未支付:", sum_unpaid
    print "未支付率：", sum_unpaid/sum_orders
    
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
    #(商家编码:J21101_1__L)
    strhead = "(商家编码:"
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
    
    in_attr = strattrib.find("(产品属性")
    in_code = strattrib.find("(商家编码")
    in_count = strattrib.find("(产品数量")
    
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
        str_list = prods.split("【")
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

#读取订单
readorders("test_sum.csv", orderlist)
#统计产品出单数，未付款数
sumorders(orderlist)
#统计国家
countrylist = country_sum(orderlist)

#统计每天数
daylist = day_sum(orderlist)

#统计产品数
sum_list = prod_sum(orderlist)

print "    国家统计    "
for key in countrylist.keys():
    print key, countrylist[key]

print "    按日统计   "
for day in daylist :
    print day

print "   按产品销量  "
#value sorted
#dict= sorted(sum_list.iteritems(), key=lambda d:d[1], reverse = True)
#key sorted
out_sum= sorted(sum_list.iteritems(), key=lambda d:d[0]) 
for s in out_sum:
    print s[0], s[1]
   



