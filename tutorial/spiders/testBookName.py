import scrapy
import sys


class doubanSpider(scrapy.Spider):
    name = 'testBookName'
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-hot']

    def parse(self, response):
        for href in response.css('table.tagCol a::attr(href)').extract():
            book_list = response.urljoin('https://book.douban.com' + href)
            # yield scrapy.Request(book_list, self.parse_bookList)

    def parse_bookList(self, response):
        with open('bookname.txt', 'w') as f:
            for info in response.css('div.info'):
                yield {
                    'bookname': info.css('a::title')
                }
                f.write(info.css('a::title')+'\n')