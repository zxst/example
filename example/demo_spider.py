from scrapy.spiders import Spider

class DemoSpider(Spider):
    name = 'demo'
    start_urls = ['http://woodenrobot.me']

    def parse(self,response):
        titles = response.xpath("//a[@class = 'post-title-link']/text()").extract()
        for title in titles:
            print title.strip()
