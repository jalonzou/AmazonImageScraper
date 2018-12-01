# -*- coding: utf-8 -*-
import scrapy
from amazonSpider.items import AmazonspiderItem

class AmazonitemlistSpider(scrapy.Spider):
    name = 'amazonItemlist'
    allowed_domains = ['www.amazon.com']

    def __init__(self, *args, **kwargs):
        super(AmazonitemlistSpider, self).__init__(*args, **kwargs)
        
        self.start_urls = []

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

        for item_detail in response.css("li.s-result-item.celwidget   > div > div > div"):
            item_price = item_detail.css("div.a-fixed-left-grid-col.a-col-right span.a-offscreen::text").extract_first()
            item_img_url = item_detail.css("div.a-fixed-left-grid-col.a-col-left > div > div > a > img").xpath("@src").extract_first()
            item_title = item_detail.css("div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small a h2::text").extract_first()
            item_href = item_detail.css("div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small a::attr(href)").extract_first()
            if item_href is not None and not item_href.startswith('http'): 
                item_href = 'https://' + self.allowed_domains[0] + item_href

            if item_href is None or item_title is None:
                continue
                
            yield AmazonspiderItem(title=item_title, price=item_price, detail_url=item_href, file_urls=[item_img_url])

        # Go to the next page.
        if self.cur_depth < self.max_depth:
            self.cur_depth += 1
            url_next = response.css("#pagnNextLink::attr(href)").extract_first()
            if url_next is not None:
                if not url_next.startswith('http'): 
                    url_next = 'https://' + self.allowed_domains[0] + url_next

                yield scrapy.Request(url_next, self.parse_list_pages)
