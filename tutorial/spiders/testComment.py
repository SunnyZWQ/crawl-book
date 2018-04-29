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
        comment = response.xpath('//*[@id="comments"]/ul/li[1]/div[2]').extract()

        with open('comment.txt','w') as f:
            f.write(str(comment))
