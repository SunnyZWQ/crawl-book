import scrapy
import sys
from tutorial.items import Book


class doubanSpider(scrapy.Spider):
    
    name = 'testEntry'

    start_urls = [
        'https://book.douban.com/subject/25862578/'
    ]

    def parse_entry(self, response):

        # book = Book()

        ############################## info from entry ############################
        ###########################################################################
        
        # title = response.css('div#info span.pl::text').extract()
        # for i in title:
        #     i.replace(':','').replace('：','')
        # content = response.css('div#info::text').extract()
        # for i in content:
        #     i.strip().replace('\n', '').replace
        
        ###########################################################################
        ###########################################################################
        

        # book['name'] = response.xpath('//*[@id="wrapper"]/h1/span')
        # book['author'] = response.xpath('//*[@id="info"]/a[1]/text()').extract()[0].strip().replace('\n','').replace(' ','')
        # book['public'] = response.xpath('//*[@id="info"]/text()[5]').extract()[0].replace(' ','')
        # book['origin_name'] = response.xpath('//*[@id="info"]/text()[7]').extract()[0].replace(' ','')
        # book['public_year'] = response.xpath('//*[@id="info"]/text()[10]').extract()[0].replace(' ','')
        # book['pages'] = response.xpath('//*[@id="info"]/text()[12]').extract()[0].replace(' ','')
        # book['price'] = response.xpath('//*[@id="info"]/text()[14]').extract()[0].replace(' ','')
        # book['book_type'] = response.xpath('//*[@id="info"]/text()[16]').extract()[0].replace(' ','')
        # book['isbn'] =  response.xpath('//*[@id="info"]/text()[20]').extract()[0].replace(' ','')
        # book['comment_link'] = response.xpath('//*[@id="content"]/div/div[1]/div[3]/div[11]/h2/span[2]/a/@href').extract[0]

        # yield book

        link = response.css('div.mod-hd h2 span.pl a::attr(href)').extract()[0]
        comment_link = response.urljoin(link)
        yield scrapy.Request(comment_link, callback=self.parse_comment)

