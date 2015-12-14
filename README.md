# ScrapyMonRg
Parsing JSON html pages of 
                  https://mon.grnet.gr/api/  with scrapy Library


Four Layers-pages of data!!!!

This progect is considered a toy project for web scraping. The https://mon.grnet.gr/api/ is a html page, consists data in JSON format. So the spider crawls the data in the forth layer of struction and then puts the native objects in a third party queue (Beanstalkd). The project uses the python client of the queue.


Total 24000+ Native Objects


Requirements 
Python 2.7
scrapy
twisted 
pyyaml
beanstalkc

OS 
Debian 8

Install beanstalkd 
1)sudo apt-get install beanstalkd 
2) pip install pyyaml 
3) pip install beanstalkc

Run Beanstalkd
beanstalkd -l 127.0.0.1 -p 11301 &

Documentation
http://beanstalkc.readthedocs.org/en/latest/tutorial.html#tube-management

Run ScrapyMonRg project
git clone git@github.com:nbompetsis/ScrapyMonRg.git
cd <ScrapyTesting>
scrapy crawl myspider



Native Object format

{
  "170735": {
    "created_timestamp": "2015-12-10 19:33:26",
    "tags": [
      "ypepth-2.grnet.gr"
    ],
    "uri": "/rg/170735/draw/static/",
    "metadata": {
      "node": {
        "name": "node",
        "value": "ypepth-2.grnet.gr"
      },
      "status": {
        "name": "status",
        "value": "up"
      },
      "nickname": {
        "name": "nickname",
        "value": "Ethernet3/26"
      },
      "name": {
        "name": "name",
        "value": "Ethernet3/26"
      },
      "upper_category_info": {
        "name": "category",
        "value": "traffic"
      },
      "description": {
        "name": "description",
        "value": "[LC-YPEPTH2-TOR02B] Physical Link to TOR2B"
      },
      "upper_domain_info": {
        "name": "domain",
        "value": "ypepth-2.grnet.gr"
      },
      "mtu": {
        "name": "mtu",
        "value": 9000
      },
      "bandwidth": {
        "name": "bandwidth",
        "value": "10.0 Gbps(9.31 Gibps) or 1.25 GBytes/s (1.16 GiBytes/s)"
      },
      "upper_node_info": {
        "name": "node",
        "value": "routers"
      },
      "type": {
        "name": "type",
        "value": "ethernetCsmacd"
      },
      "ifce_id": {
        "name": "ifce id",
        "value": 14661
      },
      "backend": {
        "name": "backend",
        "value": "mon"
      }
    }
  }
}

