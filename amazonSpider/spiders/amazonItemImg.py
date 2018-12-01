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

    def __init__(self, *args, **kwargs):
        super(AmazonitemimgSpider, self).__init__(*args, **kwargs)
        
        self.start_urls = []

        # Read Lua script running javascript on Splash.
        with open('image_click.txt', 'r') as f:
            self.script = f.read()

        # Get key words and max depth set by user.
        key_words = kwargs.get('key_words')
        max_deps = kwargs.get('max_depth')

        # Set up key words links.
        if key_words:
            for key_word in key_words:
                self.start_urls.append('https://www.amazon.com/s?url=search-alias%3Daps&field-keywords=' + key_word)
        
        # Set max crawling depth for each item.
        self.max_depth = 0 if not max_deps else max_deps

        # Initialize current depth.
        self.cur_depth = 0


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_list_pages)


    def parse_list_pages(self, response):
        # Get link to the item detail page.
        for item_info in response.css("ul#s-results-list-atf > li > div > div.a-fixed-left-grid > div"):
            item_href = item_info.css("div.a-col-right > div.a-row.a-spacing-small a::attr(href)").extract_first()

            # Format the link address.
            if not item_href.startswith('http'): 
                item_href = 'https://' + self.allowed_domains[0] + item_href

            # Scrape image on each item detail page.
            yield SplashRequest(url=item_href,
                callback=self.parse,
                endpoint='execute',
                args={'lua_source': self.script, 'timeout': 8})

        # Go to the next page.
        if self.cur_depth < self.max_depth:
            self.cur_depth += 1
            url_next = response.css("#pagnNextLink::attr(href)").extract_first()
            if not url_next.startswith('http'): 
                url_next = 'https://' + self.allowed_domains[0] + url_next

            yield scrapy.Request(url_next, self.parse_list_pages)


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
        yield AmazonspiderItem(title=item_title, price=item_price, detail_url=response.request.url, file_urls=img_urls)

        
        
