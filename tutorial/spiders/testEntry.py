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
<<<<<<< HEAD
        a = response.xpath('//*[@id="info"]/a[1]/text()').extract()[0].strip().replace('\n','').replace(' ','')
=======
        author = response.xpath('//*[@id="info"]/a[1]/text()').extract()[0].strip().replace('\n','').replace(' ','')
        public = response.xpath('//*[@id="info"]/text()[2]').extract()[0].strip().replace('\n','').replace(' ','')
>>>>>>> ed0929a470979bf21f3971095b1487a7ec5bc53c
        with open('entry.txt','w') as f:
            f.write(author + '  ' + public)



