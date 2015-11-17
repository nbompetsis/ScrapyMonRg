from ScrapyTest.items import ScrapytestItem
import scrapy
import json 

class DmozSpider(scrapy.Spider):
        name = "myspider"
        allowed_domains = ["mon.grnet.gr"]
        start_urls = ["https://mon.grnet.gr/api/rg/"]
        
        def parse(self, response):
            jsonresponse = json.loads(response.body_as_unicode())
            item = {}

            item[ScrapytestItem.SWITCHES] = jsonresponse[ScrapytestItem.SWITCHES]
            item[ScrapytestItem.ROUTERS] = jsonresponse[ScrapytestItem.ROUTERS]
            
            for itemsValue in item:
                print item[itemsValue]

            return
            
            #return item
            #filename = response.url.split("/")[-2] + '.html'
            #with open(filename, 'wb') as f:
            #   f.write(response.body)
