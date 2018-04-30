#-*- coding: UTF-8 -*-

import scrapy
import sys

class doubanSpider(scrapy.Spider):
    name = 'tagLink'
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-hot#%E6%96%87%E5%AD%A6']

    def parse(self, response):
        lista = response.css('table.tagCol a::attr(href)')
        print('list' + str(lista))
        with open('link.txt', 'w') as f:
            for href in response.css('table.tagCol a::attr(href)').extract():
                f.write('https://book.douban.com' + str(href) + '\n')
            # f.write(response.css('table.tagCol a::attr(href)'))