from ScrapyTest.items import ScrapytestItem
from urlparse import urlparse
from scrapy.http.request import Request
import scrapy
import json 
import os


class MySpider(scrapy.Spider):
        name = "myspider"
        item = {}
        item2 = {}
        item3 = {}
        resultsFolder ="./results" 
        allowed_domains = ["mon.grnet.gr"]
        domain = 'https://mon.grnet.gr'
        start_urls = ["https://mon.grnet.gr/api/rg/"]
         
        def parse(self, response):
            self.makedirResults()
            jsonresponse = json.loads(response.body_as_unicode())

            MySpider.item[ScrapytestItem.SWITCHES] = jsonresponse[ScrapytestItem.SWITCHES]
            MySpider.item[ScrapytestItem.ROUTERS] = jsonresponse[ScrapytestItem.ROUTERS]
            
            #self.createFile('layer1',self.item)
            
            for itemsValue in MySpider.item:
                itemLink =  self.domain + MySpider.item[itemsValue]
                yield Request(itemLink,callback=lambda r:self.parseLayer2(r, itemsValue))
                
            return
            


        def parseLayer2(self,response,parent):
            
            jsonresponse = json.loads(response.body_as_unicode())
            #self.createFile(parent + 'layer2',jsonresponse)
            self.item2 = jsonresponse

            for item in self.item2:
                print item
                #print jsonresponse[jsonItem]
                link3 = self.domain + self.item2[item]
                yield Request(link3,callback=lambda r:self.parseLayer3(r, item))
            return

        def parseLayer3(self,response,parent):

            jsonresponse = json.loads(response.body_as_unicode())
            print parent 
            self.createFile(parent + 'layer3',jsonresponse)

            return



        def createFile(self,namefile,results):

            try:     
                folder = os.path.join(self.resultsFolder, namefile + '.dat')
                file = open(folder, "wb")
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


