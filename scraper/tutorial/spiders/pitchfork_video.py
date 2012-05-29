'''
Created on Dec 12, 2011

@author: paul
'''
from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.utils.misc import arg_to_iter
from tutorial.items import VideoItem

class UrlArgSpider(BaseSpider):

    def __init__(self, *args, **kwargs):
        super(UrlArgSpider, self).__init__(*args, **kwargs)
        self.url=kwargs.get('url')

class PitchforkSpider(UrlArgSpider):
    name = "pitchfork-video"
    #allowed_domains = ["pitchfork.com"]

    def start_requests(self):
        reqs = []        
        ajax_url = "%s%s" % (self.url,"ajax/")  
        reqs.extend(arg_to_iter(self.make_requests_from_url(ajax_url)))
        return reqs

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        v = VideoItem()
        v['url'] = self.url
        v['artist'] = hxs.select('.//span[@class="artist"]/text()').extract()[0]
        v['title'] =  hxs.select('.//span[@class="title"]/text()').extract()[0]
        v['embed_url'] = hxs.select('//div[@class="embed"]/iframe/@src').extract()[0]
        
        # get id value from string like:
        # http://pitchfork.com/tv/musicvideos/1694-reckless-with-your-love/
        video_id = self.url.split("/")[-2].split("-")[0]
        
        image_url = "http://pitchfork-cdn.s3.amazonaws.com/video-archive/%s.jpg" % video_id
        v['image'] = image_url
        
        return v

'''
 embeded modal video
 http://pitchfork.com/tv/musicvideos/1686-a-forest-bestival-live-2011/ajax/
 

<div class="embed">
<iframe width="781" height="586" src="http://www.youtube.com/embed/1NYQo8OJAY4?fs=1&feature=oembed" frameborder="0" allowfullscreen></iframe>
</div>
<div class="nav">
    <a class="previous">&laquo;</a>
    <a class="next">&raquo;</a>
    <h3>
        <span class="artist">The Cure</span> - 
        <span class="title">A Forest (Bestival Live 2011)</span>
    </h3>
</div>

image thumbnail = http://pitchfork-cdn.s3.amazonaws.com/video-archive/1686.jpg

scrapy crawl pitchfork -a url=http://pitchfork.com/tv/musicvideos/1694-reckless-with-your-love/

''' 