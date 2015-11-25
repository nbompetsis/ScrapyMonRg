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
                #print self.first_layer
                request = Request(link_first,callback=self.parseLayer2)
                request.meta['parent'] = items_first
                yield request
            
            return
            


        def parseLayer2(self,response):

            parent = response.meta['parent']
            self.second_layer = json.loads(response.body_as_unicode())
            #self.createFile(parent + 'layer2',jsonresponse)

            for items_second in self.second_layer:
                #print item
                #print jsonresponse[jsonItem]
                link_second = self.domain + self.second_layer[items_second]
                request = Request(link_second,callback=self.parseLayer3)
                request.meta['parent'] = items_second
                yield request

            return

        def parseLayer3(self,response):

            parent = response.meta['parent'] 
            self.third_layer = json.loads(response.body_as_unicode())
            print('############################################################',parent)
            print self.third_layer            
            print '############################################################'
            
            self.createFile(parent,self.third_layer)

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


