import scrapy
import sys
#from my.items import MyscrapyItem,bookLink,book


class doubanSpider(scrapy.Spider):
    
    name = 'testEntry'

    start_urls = [
        'https://book.douban.com/subject/25862578/'
    ]

    def parse(self, response):
        # reload(sys)
        # sys.setdefaultencoding('utf-8')
        author = response.xpath('//*[@id="info"]/a[1]/text()').extract()[0].strip().replace('\n','').replace(' ','')
        public = response.xpath('//*[@id="info"]/text()[5]').extract()[0].replace(' ','')
        origin_name = response.xpath('//*[@id="info"]/text()[7]').extract()[0].replace(' ','')
        public_year = response.xpath('//*[@id="info"]/text()[10]').extract()[0].replace(' ','')
        pages = response.xpath('//*[@id="info"]/text()[12]').extract()[0].replace(' ','')
        price = response.xpath('//*[@id="info"]/text()[14]').extract()[0].replace(' ','')
        book_type = response.xpath('//*[@id="info"]/text()[16]').extract()[0].replace(' ','')
        isbn =  response.xpath('//*[@id="info"]/text()[20]').extract()[0].replace(' ','')

        with open('entry.txt','w') as f:
            f.write(author + '  ' + public + '  ' + origin_name + '  ' + public_year \
                    + '  ' + pages + '  ' + price + '  ' + book_type + '  ' + isbn)





