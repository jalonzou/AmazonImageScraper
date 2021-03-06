# Manual settings
settings = Settings()
settings['BOT_NAME'] = 'amazonSpider'
# settings['SPIDER_MODULES'] = ['amazonSpider.spiders']
settings['NEWSPIDER_MODULE'] = 'amazonSpider.spiders'
settings['ROBOTSTXT_OBEY'] = True
settings['CONCURRENT_REQUESTS'] = 2
settings['COOKIES_ENABLED'] = False
settings['SPIDER_MIDDLEWARES']['scrapy_splash.SplashDeduplicateArgsMiddleware'] = 100
settings['ITEM_PIPELINES']['scrapy.pipelines.images.FilesPipeline'] = 1
settings['FILES_STORE'] = "./output"
# settings['DOWNLOADER_MIDDLEWARES']['scrapy.downloadermiddlewares.useragent.UserAgentMiddleware'] = None
# settings['DOWNLOADER_MIDDLEWARES']['scrapy_fake_useragent.middleware.RandomUserAgentMiddleware'] = 400
settings['DOWNLOADER_MIDDLEWARES']['scrapy_splash.SplashCookiesMiddleware'] = 723
settings['DOWNLOADER_MIDDLEWARES']['scrapy_splash.SplashMiddleware'] = 725
settings['DOWNLOADER_MIDDLEWARES']['scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware'] = 810
settings['SPLASH_URL'] = 'http://localhost:8050'
settings['DUPEFILTER_CLASS'] = 'scrapy_splash.SplashAwareDupeFilter'
settings['HTTPCACHE_STORAGE'] = 'scrapy_splash.SplashAwareFSCacheStorage'