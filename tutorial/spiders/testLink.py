#-*- coding: UTF-8 -*-

import scrapy
import sys
from tutorial.items import Book

class doubanSpider(scrapy.Spider):

    # link --> booklist --> entry(写入) --> comment(写入)
    # parse    parse_list   parse_entry    parse_comment

    name = 'tagLink'
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-hot']
    book = Book()

    def parse(self, response):
        lista = response.css('table.tagCol a::attr(href)')
        book['tag'] = response.xpath('//*[@id="content"]/div/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[1]/a/text()').extract()[0]
        for href in response.css('table.tagCol a::attr(href)').extract():
            href = 'https://book.douban.com' + str(href)
            # link --> booklist
            yield scrapy.Request(href, callback=self.parse_list)

    
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

    
    def parse_entry(self, response):

        #book = Book()

        book['name'] = response.xpath('//*[@id="wrapper"]/h1/span')
        book['author'] = response.xpath('//*[@id="info"]/a[1]/text()').extract()[0].strip().replace('\n','').replace(' ','')
        book['public'] = response.xpath('//*[@id="info"]/text()[5]').extract()[0].replace(' ','')
        book['origin_name'] = response.xpath('//*[@id="info"]/text()[7]').extract()[0].replace(' ','')
        book['public_year'] = response.xpath('//*[@id="info"]/text()[10]').extract()[0].replace(' ','')
        book['pages'] = response.xpath('//*[@id="info"]/text()[12]').extract()[0].replace(' ','')
        book['price'] = response.xpath('//*[@id="info"]/text()[14]').extract()[0].replace(' ','')
        book['book_type'] = response.xpath('//*[@id="info"]/text()[16]').extract()[0].replace(' ','')
        book['isbn'] =  response.xpath('//*[@id="info"]/text()[20]').extract()[0].replace(' ','')
        book['comment_link'] = response.xpath('//*[@id="content"]/div/div[1]/div[3]/div[11]/h2/span[2]/a/@href').extract[0]

        yield book
        comment_link = response.urljoin(book['comment_link'])
        # entry --> comment
        yield scrapy.Request(comment_link, callback=self.parse_comment)