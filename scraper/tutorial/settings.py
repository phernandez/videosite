# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'tutorial'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'

#CONCURRENT_REQUESTS = 1
#DOWNLOAD_DELAY = 4
#COOKIES_DEBUG = True

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16' 

#FEED_FORMAT = "json"
#FEED_URI = "file:////home/paul/Desktop/pitchforktv.json"


ITEM_PIPELINES = ['tutorial.pipelines.MongoDBPipeline',]

#mongohq
#mongo staff.mongohq.com:10040/viddeo -u viddeo -p viddeo1
MONGODB_SERVER = "staff.mongohq.com"
MONGODB_PORT = 10040
MONGODB_DB = "viddeo"
MONGODB_COLLECTION = "videos"

#mongolab
#mongo ds033047.mongolab.com:33047/video -u video -p video1

MONGODB_URI = "mongodb://video:video1@ds033047.mongolab.com:33047/video"
MONGODB_DB = "video"
MONGODB_COLLECTION = "videos"