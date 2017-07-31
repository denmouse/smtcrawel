# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
from tutorial.items import TutorialItem




class TutorialPipeline(object):
    def __init__(self):
        dbargs = dict(
            host = '127.0.0.1',
            db = 'dbMovie',
            user = 'root',
            passwd = '107999dhp',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True, 
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb',**dbargs)
 
    def process_item(self, item, spider):
        print spider
        query = self.dbpool.runInteraction(self.insert_into_table, item)
        return item
  
    def insert_into_table(self, tx, item):
        tx.execute("insert into douban(title,movieInfo, star, quote) values(%s, %s, %s, %s)",
             (item['title'],
             item['movieInfo'],
             item['star'],
             item['quote'])
         )
	    
