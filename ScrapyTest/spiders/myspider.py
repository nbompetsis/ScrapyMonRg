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
        results_folder ="./results" 
        allowed_domains = ["mon.grnet.gr"]
        domain = 'https://mon.grnet.gr'
        start_urls = ["https://mon.grnet.gr/api/rg/"]
         
        def parse(self, response):
            self.makedirResults()
            self.nodes = json.loads(response.body_as_unicode())

            for node in self.nodes:
                link_node = self.domain + self.nodes[node]
                request = Request(link_node,callback=self.parseDomain)
                request.meta['node'] = node
                yield request
            
            return
            


        def parseDomain(self,response):

            node = response.meta['node']
            self.domains = json.loads(response.body_as_unicode())

            for dom in self.domains:
                link_dom = self.domain + self.domains[dom]
                request = Request(link_dom,callback=self.parseStatements)
                request.meta['node'] = node
                request.meta['domain'] = dom
                yield request

            return

        def parseStatements(self,response):

            node = response.meta['node']
            dom = response.meta['domain']

            self.statements = json.loads(response.body_as_unicode())
            #self.createFile(parent,self.third_layer)
            for statement in self.statements:
                link_state = self.domain + self.statements[statement]
                request = Request(link_state,callback=self.parseNativeObjects)
                request.meta['node'] = node
                request.meta['domain'] = dom
                request.meta['statement'] = statement
                yield request

            return

        
        def parseNativeObjects(self,response):


            node = response.meta['node']
            dom = response.meta['domain']
            statement = response.meta['statement']
            native_objects = {}

            native_objects = json.loads(response.body_as_unicode())
            for nat_object in native_objects:

                print '####################################################'
                self.createFile(node + '_' + dom + '_' + statement + '_' + nat_object,native_objects[nat_object])
                print '1111111111111111111111111111111111111111111111111111111111111111111111111'

            return


        def createFile(self,namefile,results):

            try:     
                print namefile
                folder = os.path.join(self.results_folder, namefile + '.dat')
                file = open(folder, "wb")
                json.dump(results,file)
                file.write('\n');
                file.close()
            except IOError:
                print("Could not write to this file!")
                pass 
  
        def makedirResults(self):

            try:     
                if not os.path.exists(self.results_folder):
                    os.makedirs(self.results_folder)
            except OSError:
                print("could not make results folder!")
                pass 


