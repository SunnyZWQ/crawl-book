import scrapy
import sys


class doubanSpider(scrapy.Spider):
    
    name = 'testComment'

    start_urls = [
        'https://book.douban.com/subject/25862578/comments/'
    ]

    def parse(self, response):
        # reload(sys)
        # sys.setdefaultencoding('utf-8')

        def rank(level):
            if level=='力荐':
                return 5
            if level=='推荐':
                return 4
            if level=='还行':
                return 3
            if level=='较差':
                return 2
            if level=='很差':
                return 1

        user = response.xpath('//*[@id="comments"]/ul/li[1]/div[2]/h3/span[2]/a/text()').extract()[0]
        rate = response.xpath('//*[@id="comments"]/ul/li[1]/div[2]/h3/span[2]/span/@title').extract()[0]
        rate = str(rank(rate))
        with open('comment.txt','w') as f:
            f.write(user + '  ' + rank(rate) + '  ')


        
        