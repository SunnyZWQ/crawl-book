import scrapy
import sys


class doubanSpider(scrapy.Spider):
    name = 'tagLink'
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-hot#%E6%96%87%E5%AD%A6']

    def parse(self, response):
        for href in response.css('table.tagCol a::attr(href)').extract():
            book_list = response.urljoin(href)
            yield scrapy.Request(book_list, self.parse)
            print(type(href))

    def parse_bookList(self,response):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        with open('bookname.txt', 'w') as f:
            for info in response.css('div.info'):
                yield {
                    'bookname': info.css('a::title')
                }
                f.write(info.css('a::title')+'\n')