#-*- coding: UTF-8 -*-

import scrapy
import sys
from tutorial.items import Book
from tutorial.items import Comment

class doubanSpider(scrapy.Spider):

    # link --> booklist --> entry(写入) --> comment(写入)
    # parse    parse_list   parse_entry    parse_comment

    name = 'tagLink'
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-hot']

    def parse(self, response):
        lista = response.css('table.tagCol a::attr(href)')
        
        with open('data/my_taglink.txt', 'a') as f:
            for href in response.css('table.tagCol a::attr(href)').extract():
                href = response.urljoin(href)
                f.write(href + '\n')
        
        for href in response.css('table.tagCol a::attr(href)').extract():
            href = response.urljoin(href)
            # link --> booklist
            yield scrapy.Request(href, callback=self.parse_list)

    
    def parse_list(self, response):
        comment = Comment()
        booklist = response.xpath('//*[@id="subject_list"]/ul/li')
        for i in booklist:
            link = i.xpath('.//div[2]/h2/a/@href').extract()[0]
            link = response.urljoin(link)
            # booklist --> entry
            yield scrapy.Request(link, callback=self.parse_entry)
        
        try:
            next_page = response.xpath('//*[@id="subject_list"]/div[2]/span[4]/a/@href').extract()[0]
            next_page = 'https://book.douban.com' + next_page
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_list)
        except Exception:
            next_page = response.xpath('//*[@id="subject_list"]/div[2]/span[3]/a/@href').extract()[0]
            next_page = 'https://book.douban.com' + next_page
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_list)
        except Exception:
            next_page = response.xpath('//*[@id="subject_list"]/div[2]/span[5]/a/@href').extract()[0]
            next_page = 'https://book.douban.com' + next_page
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_list)

    def parse_entry(self, response):

        # book = Book()

        # book['tag'] = response.xpath('').extract()[0]
        # book['name'] = response.xpath('//*[@id="wrapper"]/h1/span')
        # book['author'] = response.xpath('//*[@id="info"]/a[1]/text()').extract()[0].strip().replace('\n','').replace(' ','')
        # book['public'] = response.xpath('//*[@id="info"]/text()[5]').extract()[0].replace(' ','')
        # book['origin_name'] = response.xpath('//*[@id="info"]/text()[7]').extract()[0].replace(' ','')
        # book['public_year'] = response.xpath('//*[@id="info"]/text()[10]').extract()[0].replace(' ','')
        # book['pages'] = response.xpath('//*[@id="info"]/text()[12]').extract()[0].replace(' ','')
        # book['price'] = response.xpath('//*[@id="info"]/text()[14]').extract()[0].replace(' ','')
        # book['book_type'] = response.xpath('//*[@id="info"]/text()[16]').extract()[0].replace(' ','')
        # book['isbn'] =  response.xpath('//*[@id="info"]/text()[20]').extract()[0].replace(' ','')
        
        comment_link = response.xpath('//*[@id="content"]/div/div[1]/div[3]/div[11]/h2/span[2]/a/@href').extract()[0]

        #//*[@id="content"]/div/div[1]/div[3]/div[4]/h2/span[2]/a
        # yield self.book


        comment_link = response.urljoin(comment_link)
        # entry --> comment
        yield scrapy.Request(comment_link, callback=self.parse_comment)
    
    def parse_comment(self, response):
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
        for i in comments:
            user = i.xpath('.//div[2]/h3/span[2]/a/text()').extract()[0]
            try:
                rate = i.xpath('.//div[2]/h3/span[2]/span[1]/@title').extract()[0]
            except Exception:
                continue
            date = i.xpath('.//div[2]/h3/span[2]/span[2]/text()').extract()[0]
            rate = str(rank(rate))
            comment['book'] = book
            comment['user'] = str(user)
            comment['rate'] = rate
            comment['date'] = date
            yield comment

        next_page = response.xpath('//*[@id="content"]/div/div[1]/div/div[3]/ul/li[3]/a/@href').extract()[0]
        next_page = self.start_urls[0] + next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_comment)
