import scrapy
import sys
from tutorial.items import Comment


class doubanSpider(scrapy.Spider):
    
    name = 'testComment'

    start_urls = [
        'https://book.douban.com/subject/25862578/comments/',
        'https://book.douban.com/subject/25862578/comments/hot?p=2'
    ]

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




