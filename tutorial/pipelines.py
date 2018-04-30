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
        self.f = open('./comment.txt', 'w')
    
    def process_item(self, Comment, spider):
        #content = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        #self.f.write(content.encode("utf-8"))  #python2
        content = str(item[book]) + '\t' + str(item[user]) + '\t' + str(item[rate]) + '\t' + str(item[date]) + '\n'
        self.f.write(content)  #python3
        return Comment
    
    def close_spider(self, spider):
        self.f.close()

