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

        ###################### 如果下一页为空，则爬取下一个tag #########################
        ###########################################################################
        
        ifbook = response.css('p.pl2::text')
        if ifbook.extract()[0]=='没有找到符合条件的图书':
            print('no more booklist!')
        
        ###########################################################################
        ###########################################################################
        
        else:
            booklist = response.css('li.subject-item')

            for book in booklist:
                booklink = book.css('h2 a::attr(href)').extract()[0]
                bookname = book.css('h2 a::attr(title)').extract()[0]
                bookinfo = book.css('div.pub::text').extract()[0].replace('\n','').strip()
                img = book.css('img::attr(src)').extract()[0]
                bookrate = book.css('span.rating_nums::text').extract()[0]
                bookstar = book.css('div.star.clearfix span::attr(class)')[0].extract()
                # booklist --> entry
                yield scrapy.Request(next_page, callback=self.parse_entry)
                with open('data/my_bookinfo.txt', 'a') as f:
                    for link in booklink:
                        f.write(bookname + '    ' \
                                + booklink + '    ' \
                                + bookinfo + '    ' \
                                + img + '    ' \
                                + bookrate + '    ' \
                                + bookstar + '    ' \
                                + '\n')
        
            next_page = response.css('span.next a::attr(href)').extract()[0]
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_list)

