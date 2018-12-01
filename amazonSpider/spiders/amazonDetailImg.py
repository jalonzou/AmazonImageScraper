# -*- coding: utf-8 -*-
import sys
sys.path.append("../..")

import os
import urllib.parse
import time
import scrapy
from amazonSpider.items import AmazonspiderItem
from scrapy_splash import SplashRequest


class AmazonDetailImgSpider(scrapy.Spider):
    name = 'amazonDetailImgSpider'
    allowed_domains = ['www.amazon.com']

    def __init__(self, *args, **kwargs):
        super(AmazonDetailImgSpider, self).__init__(*args, **kwargs)
        
        self.start_urls = []

        # Read Lua script running javascript on Splash.
        with open('image_click.txt', 'r') as f:
            self.script = f.read()

        # Get key words and max depth set by user.
        item_urls = kwargs.get('item_urls')

        # Set up key words links.
        if item_urls:
            for iurl in item_urls:
                self.start_urls.append(iurl)


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                callback=self.parse,
                endpoint='execute',
                args={'lua_source': self.script, 'timeout': 8})


    def parse(self, response):
        print("parse_item_details called!")
        # Get item title.
        item_title = response.css("#productTitle::text").extract_first().strip()
        # Get item price.
        item_price = response.css("#priceblock_ourprice::text").extract_first()

        # Collect links to all images for this item.
        img_urls = list()
        for img_elements in response.css("#main-image-container > ul > li.image.item.maintain-height"):
            img_url = img_elements.css("img::attr(src)").extract_first()
            if not img_url.startswith('http'): continue
            img_urls.append(img_url)

        print('Total number of imgs:', len(img_urls))
        yield AmazonspiderItem(title=item_title, price=item_price, file_urls=img_urls)

        
        
