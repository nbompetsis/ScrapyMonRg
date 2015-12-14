"""GrMontoo Project.

Mon/Rg agent scraps the mon.grnet.gr site,
Four levels of data!

"""

from urlparse import urlparse
from scrapy.http.request import Request
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import scrapy
import json
import os
import beanstalkc
import time
import datetime


class MySpider(scrapy.Spider):
    """Crawling Spider of the GrMontoo."""

    name = "myspider"
    nodes = {}
    domains = {}
    statements = {}
    forth_layer = {}
    results_folder = "./results"
    allowed_domains = ["mon.grnet.gr"]
    domain = 'https://mon.grnet.gr'
    start_urls = ["https://mon.grnet.gr/api/rg/"]
    beanstalk = ''
    host_beanstalkd = '127.0.0.1'

    def __init__(self):
        """Init the handler for closing the spider."""
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        """First step of Mon/gr parsing."""
        try:
            # Connect to Beanstalkd server
            self.beanstalk = beanstalkc.Connection(
                    host=self.host_beanstalkd, port=11301)

            # See all tubes:
            self.beanstalk.tubes()

            # Switch to the default (tube):
            self.beanstalk.use('default')

            # self.makedirResults()
            self.nodes = json.loads(response.body_as_unicode())

            for node in self.nodes:
                link_node = self.domain + self.nodes[node]
                request = Request(link_node, callback=self.parseDomain)
                # Pass metadata to the next wave of parsing
                request.meta['node'] = node
                yield request
        except:
            print "Please run the beanstalkc"

        return

    def parseDomain(self, response):
        """Second step of Mon/rg parsing (Domains)."""
        node = response.meta['node']
        self.domains = json.loads(response.body_as_unicode())

        for dom in self.domains:
            link_dom = self.domain + self.domains[dom]
            request = Request(link_dom, callback=self.parseStatements)
            # Pass metadata to the next wave of parsing
            request.meta['node'] = node
            request.meta['domain'] = dom
            yield request

        return

    def parseStatements(self, response):
        """Third step of Mon/rg parsing (Category)."""
        node = response.meta['node']
        dom = response.meta['domain']

        self.statements = json.loads(response.body_as_unicode())
        for statement in self.statements:
            link_state = self.domain + self.statements[statement]
            request = Request(link_state, callback=self.parseNativeObjects)
            # Pass metadata to the next wave of parsing
            request.meta['node'] = node
            request.meta['domain'] = dom
            request.meta['statement'] = statement
            yield request

        return

    def parseNativeObjects(self, response):
        """Fourth step of Mon/rg parsing (Native Objects)."""
        node = response.meta['node']
        dom = response.meta['domain']
        statement = response.meta['statement']
        native_objects = {}

        native_objects = json.loads(response.body_as_unicode())
        # Change the structure of the native object
        for nat_object in native_objects:

            native_objects[nat_object]['metadata']['upper_node_info'] = {
                    "name": "node", "value": node}
            native_objects[nat_object]['metadata']['upper_domain_info'] = {
                    "name": "domain", "value": dom}
            native_objects[nat_object]['metadata']['upper_category_info'] = {
                    "name": "category", "value": statement}
            native_objects[nat_object]['metadata']['backend'] = {
                    "name": "backend", "value": "mon"}
            # Set up timestamp
            current_t = time.time()
            current_date = datetime.datetime.fromtimestamp(current_t).strftime(
                    '%Y-%m-%d %H:%M:%S')
            # native_objects[nat_object]['modified_timestamp'] = current_date
            native_objects[nat_object]['created_timestamp'] = current_date
            final_object = {}
            final_object[nat_object] = native_objects[nat_object]
            json_final_object = json.dumps(final_object)
            try:

                print '############## {} #############'.format(nat_object)
                # self.createFile(node + '_' + dom + '_' +
                # statement + '_' + nat_object,final_object)
                self.beanstalk.put(json_final_object)
                print json_final_object
                print '###############################'
            except SocketError:
                print "Please run the beanstalkc"

        return

    def spider_closed(self, reason):
        """Closing Handler."""
        # self.beanstalk.put('quit')
        if reason == 'finished':
            print 'quit'
        elif reason == 'shutdown':
            print 'control C pressed'
        elif reason == 'cancelled':
            print 'Reason cancelled'
        else:
            print reason

    def createFile(self, namefile, results):
        """Create File with Native Objects."""
        try:
            print namefile
            folder = os.path.join(self.results_folder, namefile + '.dat')
            file = open(folder, "wb")
            json.dump(results, file)
            file.write('\n')
            file.close()
        except IOError:
            print("Could not write to this file!")
            pass

    def makedirResults(self):
        """Make fodler."""
        try:
            if not os.path.exists(self.results_folder):
                os.makedirs(self.results_folder)
        except OSError:
            print("could not make results folder!")
            pass
