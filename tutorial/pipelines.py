# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class CommentPipeline(object):
    
    """生成txt文件!"""
    
    def open_spider(self, spider):
        self.f = open('data/comment.txt', 'w')
    
    def process_item(self, Comment, spider):
        content = str(Comment['book']) + '\t' + str(Comment['user']) + '\t' + str(Comment['rate']) + '\t' + str(Comment['date']) + '\n'
        self.f.write(content)  #python3
        return Comment
    
    def close_spider(self, spider):
        self.f.close()


class BookPipeline(object):
    
    """生成txt文件!"""
    
    def open_spider(self, spider):
        self.f = open('data/book.txt', 'w')
    
    def process_item(self, Book, spider):
        content = str(Book['name']) + '\t' \
                 + str(Book['tag']) + '\t' \
                 + str(Book['author'])  + '\t' \
                 + str(Book['public']) + '\t' \
                 + str(Book['origin_name']) + '\t' \
                 + str(Book['public_year']) + '\t' \
                 + str(Book['pages']) + '\t' \
                 + str(Book['price']) + '\t' \
                 + str(Book['book_type']) + '\t' \
                 + str(Book['isbn']) + '\n'
        self.f.write(content)
        return Book
    
    def close_spider(self, spider):
        self.f.close()
