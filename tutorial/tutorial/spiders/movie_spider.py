
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from tutorial.items import TutorialItem

class Movie(CrawlSpider):
    name = "movie"
    redis_key = 'douban:start_urls'
    start_urls = ['http://movie.douban.com/top250']

    url = 'http://movie.douban.com/top250'

    def parse(self,response):
        # print response.body
        item = TutorialItem()
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="info"]')
        for eachMoive in Movies:
            title = eachMoive.xpath('div[@class="hd"]/a/span/text()').extract()
            fullTitle = ''
            for each in title:
                fullTitle += each
            movieInfo = eachMoive.xpath('div[@class="bd"]/p/text()').extract()
            star = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['title'] = fullTitle
            item['movieInfo'] = ';'.join(movieInfo)
            item['star'] = star
            item['quote'] = quote
            yield item
        nextLink = selector.xpath('//span[@class="next"]/a/@href')
        if nextLink:
            url = response.urljoin(nextLink[0].extract())
            print url
            yield Request(url,self.parse)

