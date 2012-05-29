'''
Created on Dec 12, 2011

@author: paul
'''
from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from selenium import webdriver
from scrapy.spider import BaseSpider
from scrapy.utils.misc import arg_to_iter
from tutorial.items import VideoItem
    
class PitchforkTVMusicSpider(BaseSpider):
    name = "pitchforktv"
    allowed_domains = ["pitchfork.com"]
    start_urls = [
        "http://pitchfork.com/tv/musicvideos/",
    ]

    def parse(self, response):
        
        hxs = HtmlXPathSelector(response)
        
        """
        <ul class="object-grid archivevideo-grid"> 
        """
        
        video_content = hxs.select('//ul[@class="object-grid archivevideo-grid"]//li')
        self.log("Found %s videos in response" % len(video_content))
        
        for video in video_content:
            
            #driver = webdriver.Firefox()
            
            """
            <li class=" "> 
                <a href="/tv/musicvideos/1987-my-better-self/"> 
                    <div class="artwork"> 
                        <span class="image" data-src="http://cdn2.pitchfork.com/video-archive/1987/medium.8b9e0e7c.jpg"></span> 
                    </div> 
                    <div class="info"> 
                        <h1 class="artist">Tennis</h1> 
                        <h2 class="title">My Better Self</h2> 
                    </div> 
                </a> 
            </li>
            
            """
            v = VideoItem()
            v['url'] = "http://pitchfork.com" + video.select('.//a/@href').extract()[0]
            v['artist'] = video.select('.//h1[@class="artist"]/text()').extract()[0]
            v['title'] =  video.select('.//h2[@class="title"]/text()').extract()[0]
            v['image'] =  video.select('.//span[@class="image"]/@data-src').extract()[0]
            
            # parse detail with selenium
            try:
                v['embed_url'] = parse_detail_with_selenium(self.driver, v['url'])
            except Exception:
                print "Exception processing item %s" % v                
            
            #driver.quit()
            yield v
        
        # iterate through pages
        for next_page in hxs.select('//a[@class="next"]/@href').extract():
            self.log("Following next page to %s." % next_page)
            yield Request("http://pitchfork.com" + next_page, callback=self.parse)
        
        # close selenium
        #self.driver.quit()
        
    def __init__(self, *args, **kwargs):
        # selenium driver
        self.driver = webdriver.Firefox()
        
def parse_detail_with_selenium(driver, url):
    driver.get(url)
    
    # look for iframes first
    iframes = driver.find_elements_by_xpath('//iframe')
    if iframes:        
        iframe_src_attrs = [iframe.get_attribute('src') for iframe in iframes]
        # print "Found iframe src = %s" % iframe_src_attrs
        for i in iframe_src_attrs:
            if "vimeo" in i:
                return i
            if "youtube" in i:
                return i
            
    # look for embed objects        
    driver.find_element_by_xpath('//div[@class="embed"]')
    divembed = driver.find_element_by_xpath('//div[@class="embed"]')
    embed = divembed.find_element_by_xpath('//embed')
    embed_src = embed.get_attribute('src')    
    return embed_src

'''
 youtube embed modal video
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
