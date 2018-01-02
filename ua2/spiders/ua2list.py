# -*- coding: utf-8 -*-
import scrapy
from ua2.items import Ua2Item
import lxml
import urllib
import re

class Ua2listSpider(scrapy.Spider):
    name = 'ua2list'
    allowed_domains = ['udger.com']
#    start_urls = ['https://udger.com/resources/ua-list']

    def __init__(self):
        self.start_urls = []
        self.entry_url = 'https://udger.com/resources/ua-list'
        self.link_xpath = '//tr//a[contains(@href, "/resources/ua-list/browser-detail?")]/@href'
        self.init_ua = ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; 2345Explorer 5.0.0.14136)')
#        item['browser'] = response.xpath('//tr//a[contains(@href, "/resources/ua-list/browser-detail?")]/text()').extract()[0]
#        item['useragent_link'] = response.xpath('//tr//a[contains(@href, "/resources/ua-list/browser-detail?")]/@href').extract()[0]

    def start_requests(self):
        opener = urllib.request.build_opener()
        opener.addheaders = [self.init_ua]
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(self.entry_url).read().decode('utf-8')
        self.selector = lxml.etree.HTML(data)
        links = self.selector.xpath(self.link_xpath)

        for v in links:
            prefix = 'https://udger.com' + re.sub('\s', '%20', v)
            self.start_urls.append(prefix)
        yield scrapy.Request(self.start_urls[0], callback=self.parse, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; 2345Explorer 5.0.0.14136)'})

    def parse(self, response):
        item = Ua2Item()
        item['name'] = response.xpath('//td/p/a[contains(@href, "/resources/online-parser?")]/text()').extract()
        if item['name'] != []:
            next_ua = item['name'][0]
        else:
            next_ua = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; 2345Explorer 5.0.0.14136)'

        yield item

        for i in range(1, (len(self.start_urls))):
            print('use agent : %s'%next_ua)
            yield scrapy.Request(self.start_urls[i], callback  = self.parse, 
            headers = {'User-Agent': next_ua})
