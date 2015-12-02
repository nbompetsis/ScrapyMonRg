from urlparse import urlparse
from scrapy.http.request import Request
from scrapy.xlib.pydispatch import dispatcher
import scrapy
import json 
import os
import beanstalkc

class MySpider(scrapy.Spider):
        name = "myspider"
        nodes = {}
        domains = {}
        statements = {}
        forth_layer = {}
        results_folder = "./results" 
        allowed_domains = ["mon.grnet.gr"]
        domain = 'https://mon.grnet.gr'
        start_urls = ["https://mon.grnet.gr/api/rg/"]
        beanstalk = '' #beanstalkc.Connection(host='127.0.0.1', port=11301)
        host_beanstalkd = '127.0.0.1'

        def parse(self, response):

            # Connect to Beanstalkd server
            self.beanstalk = beanstalkc.Connection(host=self.host_beanstalkd, port=11301)
            
            # See all tubes:
            self.beanstalk.tubes()

            # Switch to the default (tube):
            self.beanstalk.use('default')


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

                native_objects[nat_object]['metadata']['upper_node_info'] = {"name":"node", "value":node}
                native_objects[nat_object]['metadata']['upper_domain_info'] = {"name":"domain", "value":dom}
                native_objects[nat_object]['metadata']['upper_category_info'] = {"name":"category", "value":statement}
                native_objects[nat_object]['metadata']['backend'] = {"name":"backend", "value":"mon"}
                final_object = {}
                final_object[nat_object] = native_objects[nat_object]
                json_final_object = json.dumps(final_object)

                print '##########################################################################################'
                self.createFile(node + '_' + dom + '_' + statement + '_' + nat_object,final_object)
                self.beanstalk.put(json_final_object)
                print json_final_object
                print '##########################################################################################'

            return

        def spider_closed(self,reason):
            if reason == 'finished':
                print 'QUITTTTTTTTTTTTTTT'
                self.beanstalk.put('quit')


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


