import scrapy
import sys
#from my.items import MyscrapyItem,bookLink,book


class doubanSpider(scrapy.Spider):
    name = 'testEntry'

    start_urls = [
        'https://book.douban.com/subject/25862578/'
    ]

    def parse(self, response):
        #reload(sys)
        #sys.setdefaultencoding('utf-8')
        #a = response.xpath('//*[@id="info"]/a[1]').extract().strip().replace('<*>','')
        a = response.xpath('//*[@id="info"]/a[1]/text()').extract()[0].strip().replace('\n','').replace(' ','')
        with open('entry.txt','w') as f:
            f.write(a)
