# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Ua2Pipeline(object):

    def __init__(self):
        try:
            self.file = open('C:\\programlearn\\scrapy\\ua2\\allua.txt', 'a', encoding='utf-8')
        except IOError as e:
            print('open error : %s'%(str(e)))
        

    def process_item(self, item, spider):
        for v in item['name']:
            print('save: %s' % v)
            self.file.write('\'' + v + '\',\r\n')
        self.file.flush()    
        return item

    def close_spider(self, spider):
        self.file.close()
