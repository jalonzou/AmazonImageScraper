# -*- coding: utf-8 -*-
import scrapy
from amazonSpider.items import AmazonspiderItem

class AmazonitemlistSpider(scrapy.Spider):
    name = 'amazonItemlist'
    allowed_domains = ['www.amazon.com/']
    start_urls = ['https://www.amazon.com/s?url=search-alias%3Daps&field-keywords=box']

    def parse(self, response):
        for item_detail in response.css("li.s-result-item.celwidget   > div > div > div"):
            item_price = item_detail.css("div.a-fixed-left-grid-col.a-col-right span.a-offscreen::text").extract_first()
            item_img_url = item_detail.css("div.a-fixed-left-grid-col.a-col-left > div > div > a > img").xpath("@src").extract_first()
            item_title = item_detail.css("div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small a h2::text").extract_first()
            yield AmazonspiderItem(title=item_title, price=item_price, file_urls=[item_img_url])