# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymongo
from scrapy.exceptions import DropItem
from scrapy import log

class JobsearchPipeline(object):
    def __init__(self):
        self.coon = pymongo.MongoClient(host=settings['MONGODB_HOST'],port=settings['MONGODB_PORT'])
        self.db = self.coon[settings['MONGODB_DBNAME']]
        self.coll = self.db[settings['MONGODB_COLLECTIONNAME']]
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missming{}!'.format(data))
        if valid:
            self.coll.insert(dict(item))
            log.msg('item added to mongodb database !',level=log.DEBUG,spider=spider)

        return item
