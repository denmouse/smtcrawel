from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from amazon.items import AmazonItem

import time
from datetime import *
import re
import string
import codecs


class AmazonSpider(CrawlSpider):
	name = "sort"
	searchword = 'mini skirt'
	start_urls = ['http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=mini+skirt&rh=i%3Aaps%2Ck%3Amini+skirt']
	sort_whole = 0
	now_time = datetime.now()
	sort_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
	#1. get page 
	#2, get asin , sort, title
	# get next page
	def __init__(self):
		self.sort_whole = 0

	def parse(self,response):
        # print response.body
		item = AmazonItem()
		selector = Selector(response)
		
		#page number 
		page_num = 0
		page  = selector.xpath('//div[@id="pagn"]/span[@class="pagnCur"]/text()').extract()
		if page:
			page_num = int(page[0])

		#sort in page

		products = selector.xpath('//li[starts-with(@id,"result_")]')
		for prod in products: 
			prod_asin = prod.xpath('@data-asin').extract()
			number_str = prod.xpath('@id').extract()
			sort_in_page = number_str[0][7:]

			prod_title = prod.xpath('div/div[3]/div[1]/a/h2/text()').extract()
			#print prod_title, prod_asin,sort_in_page,self.sort_whole
			 
			item['keyword'] = self.searchword
			#item['sort'] = self.sort_whole + int(sort_in_page)
		
			self.sort_whole = self.sort_whole + 1
			item['sort'] = self.sort_whole
			item['page'] = page_num
			item['asin'] = prod_asin
			item['time'] = self.sort_time
			yield item
	
		#self.sort_whole = self.sort_whole + int(sort_in_page)
		pg_next  = selector.xpath('//div[@id="pagn"]/span[@class="pagnRA"]')
		if pg_next:

			nexturl = selector.xpath('//div[@id="pagn"]/span[@class="pagnRA"]/a/@href')
			url = response.urljoin(nexturl[0].extract())
			print url
			yield Request(url,self.parse)
		
