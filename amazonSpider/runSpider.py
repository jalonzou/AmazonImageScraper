# from twisted.internet import reactor
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.project import get_project_settings
# from scrapy.utils.log import configure_logging
# from amazonItemImg import AmazonitemimgSpider

# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# runner = CrawlerRunner(get_project_settings())

# mySpider = AmazonitemimgSpider('piano', 1)
# runner.crawl(mySpider)
# d = runner.join()
# d.addBoth(lambda _: reactor.stop())

# reactor.run()

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from amazonItemImg import AmazonitemimgSpider
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

process = CrawlerProcess(settings)

mySpider = AmazonitemimgSpider('piano', 2)
print(mySpider.start_urls)
process.crawl(mySpider)
process.start(stop_after_crawl=False)