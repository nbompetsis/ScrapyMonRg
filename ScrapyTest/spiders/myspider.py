from ScrapyTest.items import ScrapytestItem
import scrapy
import json 
import os



class MySpider(scrapy.Spider):
        name = "myspider"
        item = {}
        resultsFolder ="./results" 
        allowed_domains = ["mon.grnet.gr"]
        start_urls = ["https://mon.grnet.gr/api/rg/"]
         
        def parse(self, response):
            self.makedirResults()
            jsonresponse = json.loads(response.body_as_unicode())

            MySpider.item[ScrapytestItem.SWITCHES] = jsonresponse[ScrapytestItem.SWITCHES]
            MySpider.item[ScrapytestItem.ROUTERS] = jsonresponse[ScrapytestItem.ROUTERS]
            
            for itemsValue in MySpider.item:
                print MySpider.item[itemsValue]


            self.createFile(layer1,self.item)
            return
            



        def makedirResults(self):

            try:     
                if not os.path.exists(self.resultsFolder):
                    os.makedirs(self.resultsFolder)
            except OSError:
                print("Could not make results folder!")
                pass 


        def createFile(self,namefile,results):

            try:     
                file = open(self.resultsFolder + namefile + '.dat',"wb")

                for iterat in results:
                    file.write( "Python is a great language.\nYeah its great!!\n");
            except IOError:
                print("Could not write to this file!")
                pass 


            #return item
            #filename = response.url.split("/")[-2] + '.html'
            #with open(filename, 'wb') as f:
            #   f.write(response.body)
