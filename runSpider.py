import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from user_config import *
from amazonSpider.spiders.amazonItemImg import AmazonitemimgSpider
from amazonSpider.spiders.amazonItemlist import AmazonitemlistSpider
from amazonSpider.spiders.amazonDetailImg import AmazonDetailImgSpider

# Read user settings
if not KEY_WORDS:
    raise KeyError('No key word has been provided.')

if not MAX_DEPTH:
    MAX_DEPTH = 0

if DETAIL_IMG is None:
    raise KeyError('DETAIL_IMG is not defined.')

settings = get_project_settings()

# Set output format and filename.
settings['FEED_FORMAT'] = 'json'
settings['FEED_URI'] = 'output/result.json'

process = CrawlerProcess(settings)

# Create spider process.
if DETAIL_IMG:
    process.crawl(AmazonitemimgSpider, key_words=KEY_WORDS, max_depth=MAX_DEPTH)
else:
    process.crawl(AmazonitemlistSpider, key_words=KEY_WORDS, max_depth=MAX_DEPTH)


# Fire the process.
process.start()
