from ScrapyTest.items import ScrapytestItem
from urlparse import urlparse
from scrapy.http.request import Request
import scrapy
import json 
import os


class MySpider(scrapy.Spider):
        name = "myspider"
        first_layer = {}
        second_layer = {}
        third_layer = {}
        forth_layer = {}
        resultsFolder ="./results" 
        allowed_domains = ["mon.grnet.gr"]
        domain = 'https://mon.grnet.gr'
        start_urls = ["https://mon.grnet.gr/api/rg/"]
         
        def parse(self, response):
            self.makedirResults()
            jsonresponse = json.loads(response.body_as_unicode())

            self.first_layer[ScrapytestItem.SWITCHES] = jsonresponse[ScrapytestItem.SWITCHES]
            self.first_layer[ScrapytestItem.ROUTERS] = jsonresponse[ScrapytestItem.ROUTERS]
            
            #self.createFile('layer1',self.item)
            
            for items_first in self.first_layer:
                link_first =  self.domain + self.first_layer[items_first]
                yield Request(link_first,callback=lambda r:self.parseLayer2(r, items_first))
                
            return
            


        def parseLayer2(self,response,parent):
            
            self.second_layer = json.loads(response.body_as_unicode())
            #self.createFile(parent + 'layer2',jsonresponse)

            for items_second in self.second_layer:
                #print item
                #print jsonresponse[jsonItem]
                link_second = self.domain + self.second_layer[items_second]
                yield Request(link_second,callback=lambda r:self.parseLayer3(r, items_second))
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


