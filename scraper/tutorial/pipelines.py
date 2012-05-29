# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import pymongo

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log

class MongoDBPipeline(object):
    def __init__(self):
        """
        >>> connection = Connection('mongodb://video:video1@ds033047.mongolab.com:33047/video')
        >>> db = connection.video
        >>> collection = db.videos
        """
        connection = pymongo.Connection("mongodb://video:video1@ds033047.mongolab.com:33047/video")
        db = connection.video
        self.collection = db.videos
        
    def process_item(self, item, spider):
        valid = True
        for data in item:
            # here we only check if the data is not null
            # but we could do any crazy validation we want
            if not data:
                valid = False
                raise DropItem("Missing %s of blogpost from %s" % (data, item['url']))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Item added to MongoDB database %s/%s" % 
                    (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                    level=log.DEBUG, spider=spider) 
        return item
