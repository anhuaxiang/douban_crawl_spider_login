from scrapy import cmdline
cmdline.execute("scrapy crawl douban_spider -o douban_spider.csv".split())