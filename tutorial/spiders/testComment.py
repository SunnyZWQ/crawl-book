import scrapy
import sys
from tutorial.items import Comment


class doubanSpider(scrapy.Spider):
    
    name = 'testComment'

    start_urls = [
        'https://book.douban.com/subject/25862578/comments/',
        'https://book.douban.com/subject/25862578/comments/hot?p=2'
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

        comment = Comment()
        book = response.xpath('//*[@id="content"]/div/div[2]/div/p[2]/a/text()').extract()[0]
        comments = response.xpath('//*[@id="comments"]/ul/li')
        with open('comment.txt','w') as f:
            for i in comments:
                user = i.xpath('.//div[2]/h3/span[2]/a/text()').extract()[0]
                try:
                    rate = i.xpath('.//div[2]/h3/span[2]/span[1]/@title').extract()[0]
                except Exception:
                    continue
                date = i.xpath('.//div[2]/h3/span[2]/span[2]/text()').extract()[0]
                rate = str(rank(rate))
                # f.write(book + '  ' + str(user) + '  ' + rate + '  ' + date + '\n')
                comment['book'] = book
                comment['user'] = str(user)
                comment['rate'] = rate
                comment['date'] = date
                yield comment

            next_page = response.xpath('//*[@id="content"]/div/div[1]/div/div[3]/ul/li[3]/a/@href').extract()[0]
            next_page = self.start_urls[0] + next_page
            
            # if next_page is not None:
            #     next_page = response.urljoin(next_page)
            #     yield scrapy.Request(next_page, callback=self.parse)




