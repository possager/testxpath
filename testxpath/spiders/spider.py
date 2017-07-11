import scrapy
from testxpath import deal_response



class test_spider(scrapy.Spider):
    name = 'spider1'
    start_urls=['http://sn.newssc.org/system/20170418/002159156.html']

    def parse(self, response):
        # print response.body
        thisclass=deal_response.deal_response(response)
        print thisclass
        print 'this'