from ScrapyTest.items import ScrapytestItem
from urlparse import urlparse
from scrapy.http.request import Request
import scrapy
import json 
import os


class MySpider(scrapy.Spider):
        name = "myspider"
        item = {}
        resultsFolder ="./results" 
        allowed_domains = ["mon.grnet.gr"]
        domain = 'https://mon.grnet.gr'
        start_urls = ["https://mon.grnet.gr/api/rg/"]
         
        def parse(self, response):
            self.makedirResults()
            jsonresponse = json.loads(response.body_as_unicode())

            MySpider.item[ScrapytestItem.SWITCHES] = jsonresponse[ScrapytestItem.SWITCHES]
            MySpider.item[ScrapytestItem.ROUTERS] = jsonresponse[ScrapytestItem.ROUTERS]
            
            self.createFile('layer1',self.item)
            
            for itemsValue in MySpider.item:
                itemLink =  self.domain + MySpider.item[itemsValue]
          #      yield Request(itemLink, callback = self.parseItem, {'parent': itemsValue})
                yield Request(itemLink,callback=lambda r:self.parseItem(r, itemsValue))


            return
            


        def parseItem(self,response,parent):
            
            jsonresponse = json.loads(response.body_as_unicode())
            self.createFile(parent + 'layer2',jsonresponse)
 
            return



        def createFile(self,namefile,results):

            try:     
                folder = os.path.join(self.resultsFolder, namefile + '.dat')
                file = open(folder, "wb")
                print folder
                json.dump(results,file)
                file.write('\n');
                file.close()
            #    for res in results:
            #        file.write( res + ' , ' + results[res] + '\n');  

            except IOError:
                print("Could not write to this file!")
                pass 
  
        def makedirResults(self):

            try:     
                if not os.path.exists(self.resultsFolder):
                    os.makedirs(self.resultsFolder)
            except OSError:
                print("could not make results folder!")
                pass 


