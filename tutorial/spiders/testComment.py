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
                return '5'
            if level=='推荐':
                return '4'
            if level=='还行':
                return '3'
            if level=='较差':
                return '2'
            if level=='很差':
                return '1'

        book = response.xpath('//*[@id="content"]/div/div[2]/div/p[2]/a/text()').extract()[0]
        comments = response.xpath('//*[@id="comments"]/ul/li')
        i = 1
        while(comments[i] is not None):
        # for item in comments:
            user = item.xpath('.//div[2]/h3/span[2]/a/text()').extract()[0]
            rate = item.xpath('.//div[2]/h3/span[2]/span[1]/@title').extract()[0]
            date = item.xpath('.//div[2]/h3/span[2]/span[2]/text()').extract()[0]
            rate = str(rank(rate))
            with open('comment.txt','w') as f:
                f.write(book + '  ' + str(user) + '  ' + rate + '  ' + date + '\n')
            i++

        next_page = response.xpath('//*[@id="content"]/div/div[1]/div/div[3]/ul/li[3]/a/@href').extract()[0]
        next_page = self.start_urls[0] + next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


