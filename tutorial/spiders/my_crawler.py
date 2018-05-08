#-*- coding: UTF-8 -*-

import scrapy
import sys
from tutorial.items import Book
from tutorial.items import Comment

class doubanSpider(scrapy.Spider):

    # link --> booklist --> entry(写入) --> comment(写入)
    # parse    parse_list   parse_entry    parse_comment

    name = 'my'
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
                with open('data/my_bookinfo.txt', 'a') as f:
                    f.write(bookname + '    ' \
                            + booklink + '    ' \
                            + bookinfo + '    ' \
                            + img + '    ' \
                            + bookrate + '    ' \
                            + bookstar + '    ' \
                            + '\n')
                # booklist --> entry
                yield scrapy.Request(booklink, callback=self.parse_entry)
        
            next_page = response.css('span.next a::attr(href)').extract()[0]
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_list)


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


        listcomment = response.css('div.comment')
        bookname = response.css('p.pl2.side-bar-link a::text').extract()[1]

        for comment in listcomment:
            userrank = comment.css('span::attr(title)').extract()[0]
            userrank = rank(userrank)
            username = comment.css('h3 span a::text').extract()[1]

            with open('data/mycomment.txt') as f:
                f.write(bookname + '    ' \
                        + username + '    ' \
                        + userrank + '    ' \
                        + '\n')
        
        # name_rank：长度为40的list（下标0-39），(下标从1)奇数位为评分，偶数位为评论者

        # comment = Comment()
        # book = response.xpath('//*[@id="content"]/div/div[2]/div/p[2]/a/text()').extract()[0]
        # comments = response.xpath('//*[@id="comments"]/ul/li')
        # with open('comment.txt','w') as f:
        #     for i in comments:
        #         user = i.xpath('.//div[2]/h3/span[2]/a/text()').extract()[0]
        #         try:
        #             rate = i.xpath('.//div[2]/h3/span[2]/span[1]/@title').extract()[0]
        #         except Exception:
        #             continue
        #         date = i.xpath('.//div[2]/h3/span[2]/span[2]/text()').extract()[0]
        #         rate = str(rank(rate))
        #         # f.write(book + '  ' + str(user) + '  ' + rate + '  ' + date + '\n')
        #         comment['book'] = book
        #         comment['user'] = str(user)
        #         comment['rate'] = rate
        #         comment['date'] = date
        #         yield comment

        # next_page = response.xpath('//*[@id="content"]/div/div[1]/div/div[3]/ul/li[3]/a/@href').extract()[0]
        # next_page = self.start_urls[0] + next_page

        next_page = response.css('a.page-btn::attr(href)').extract()[0]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_comment)
