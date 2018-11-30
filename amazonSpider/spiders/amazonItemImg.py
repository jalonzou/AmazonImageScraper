# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")

import os
import urllib.parse
import time
import scrapy
from amazonSpider.items import AmazonspiderItem
from scrapy_splash import SplashRequest


class AmazonitemimgSpider(scrapy.Spider):
    name = 'amazonItemImg'
    allowed_domains = ['www.amazon.com']

    def __init__(self, key_words='table', max_depth = 0, *args, **kwargs):
        super(AmazonitemimgSpider, self).__init__(*args, **kwargs)
        with open('script_item_img.txt', 'r') as f:
            self.script = f.read()
        self.start_urls = []
        self.start_urls.append('https://www.amazon.com/s?url=search-alias%3Daps&field-keywords=' + key_words)
        self.max_depth = max_depth
        self.cur_depth = 0


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_list_pages)
            # yield SplashRequest(url=url,
            #     callback=self.parse_list_pages,
            #     endpoint='render.html',)


    def parse_list_pages(self, response):
        # print(len(response.css("ul#s-results-list-atf > li > div > div > div")))
        for item_info in response.css("ul#s-results-list-atf > li > div > div.a-fixed-left-grid > div"):
            item_href = item_info.css("div.a-col-right > div.a-row.a-spacing-small a::attr(href)").extract_first()
            # print(item_info.extract())
            # print(item_href)

            if not item_href.startswith('http'): 
                item_href = 'http://' + self.allowed_domains[0] + item_href
            elif item_href.startswith('https'):
                item_href = item_href[:4] + item_href[5:]

            # yield scrapy.Request(item_href, self.parse)
            yield SplashRequest(url=item_href,
                callback=self.parse,
                endpoint='execute',
                args={'lua_source': self.script, 'timeout': 5})

        if self.cur_depth < self.max_depth:
            self.cur_depth += 1
            url_next = response.css("#pagnNextLink::attr(href)").extract_first()
            if not url_next.startswith('http'): 
                url_next = 'https://' + self.allowed_domains[0] + url_next
            # print(url_next, "nainai")
            yield scrapy.Request(url_next, self.parse_list_pages)


    def parse(self, response):
        print("parse_item_details called!")
        item_title = response.css("#productTitle::text").extract_first().strip()
        item_price = response.css("#priceblock_ourprice::text").extract_first()

        img_urls = list()
        for img_elements in response.css("#main-image-container > ul > li.image.item.maintain-height"):
            img_url = img_elements.css("img::attr(src)").extract_first()
            if not img_url.startswith('http'): continue
            img_urls.append(img_url)

        print('Total number of imgs:', len(img_urls))
        yield AmazonspiderItem(title=item_title, price=item_price, file_urls=img_urls)

        
        
