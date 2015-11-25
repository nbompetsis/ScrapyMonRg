from ScrapyTest.items import ScrapytestItem
from urlparse import urlparse
from scrapy.http.request import Request
from ScrapyTest.items import RgItem
import scrapy
import json 
import os


class MySpider(scrapy.Spider):
        name = "myspider"
        nodes = {}
        domains = {}
        statements = {}
        forth_layer = {}
        resultsFolder ="./results" 
        allowed_domains = ["mon.grnet.gr"]
        domain = 'https://mon.grnet.gr'
        start_urls = ["https://mon.grnet.gr/api/rg/"]
         
        def parse(self, response):
            self.makedirResults()
            self.nodes = json.loads(response.body_as_unicode())

            #self.createFile('layer1',self.item)
            #rgItem = RgItem()
            for node in self.nodes:
                #rgItem = RgItem()
                #rgItem['node'] = node
                link_node = self.domain + self.nodes[node]
                request = Request(link_node,callback=self.parseDomain)
                #request.meta['node'] = items_first
                request.meta['node'] = node
                yield request
            
            return
            


        def parseDomain(self,response):

            node = response.meta['node']
            self.domains = json.loads(response.body_as_unicode())
            #self.createFile(parent + 'layer2',jsonresponse)
            #print('Layer1############################################################',rgResponse['node'])

            for dom in self.domains:
                #print item
                #print jsonresponse[jsonItem
                link_dom = self.domain + self.domains[dom]
                request = Request(link_dom,callback=self.parseStatements)
                request.meta['node'] = node
                request.meta['domain'] = dom
                yield request

            return

        def parseStatements(self,response):

            node = response.meta['node']
            dom = response.meta['domain']

            statements = json.loads(response.body_as_unicode())
            #self.createFile(parent,self.third_layer)
            

            
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


