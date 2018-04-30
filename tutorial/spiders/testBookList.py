import scrapy
import sys
from tutorial.items import Book


class doubanSpider(scrapy.Spider):
    
    # link --> booklist --> entry(写入) --> comment(写入)
    name = 'testBookList'

    start_urls = [
        'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4'
    ]

    def parse_list(self, response):
        comment = Comment()
        booklist = response.xpath('//*[@id="subject_list"]/ul/li')
        for i in booklist:
            link = i.xpath('.//div[2]/h2/a').extract()[0]
            link = response.urljoin(link)
            # booklist --> entry
            yield scrapy.Request(next_page, callback=self.parse_entry)
        
        next_page = response.xpath('//*[@id="subject_list"]/div[2]/span[4]/a/@href').extract()[0]
        next_page = 'https://book.douban.com' + next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_list)

