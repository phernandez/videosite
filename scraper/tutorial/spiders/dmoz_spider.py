from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from tutorial.items import DmozItem

class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        
        print("ARG1=%s" % self.arg1)
        
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ul/li')
        items = []
        for site in sites:
            item = DmozItem()
            item['title'] = site.select('a/text()').extract()
            item['link'] = site.select('a/@href').extract()
            item['desc'] = site.select('text()').extract()
            items.append(item)
            return items
        
    def __init__(self, *args, **kwargs):
        super(DmozSpider, self).__init__(*args, **kwargs)
        self.arg1=kwargs.get('arg1',"default value") 