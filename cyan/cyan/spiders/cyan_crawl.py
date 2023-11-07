import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CyanCrawlSpider(CrawlSpider):
    name = "cyan_crawl"
    allowed_domains = ["cian.ru"]
    start_urls = [
        "https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p=2&region=1&type=4",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        links = response.xpath(
            '//*[@id="frontend-serp"]/div/div[4]/div/article/div[1]/div/div[1]/div/a/@href'
        ).extract()
        for link in links:
            yield response.follow(link, callback=self.parse_item)

        next_page = response.xpath(
            '//*[@id="frontend-serp"]/div/div[5]/div[1]/nav/a[2]/@href'
        ).extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    """rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths='//*[@id="frontend-serp"]/div/div[4]/div/article/div[1]/div/div[1]/div/a'
            ),
            callback="parse_item",
            follow=True,
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths='//*[@id="frontend-serp"]/div/div[5]/div[1]/nav/a[2]'
            )
        ),
    )"""

    def parse_item(self, response):
        item = {}
        item["title"] = response.xpath(
            '//*[@id="frontend-offer-card"]/div[2]/div[2]/section/div/div/div[1]/h1/text()'
        ).get()
        item["price"] = response.xpath(
            '//*[@id="frontend-offer-card"]/div[2]/div[3]/div/div[1]/div[1]/div[1]/div[3]/div/div[1]/span/text()'
        ).get()
        item["district"] = response.xpath(
            '//*[@id="frontend-offer-card"]/div[2]/div[2]/section/div/div/div[2]/address/div/div/a[2]/text()'
        ).get()
        item["area"] = response.xpath(
            '//*[@id="frontend-offer-card"]/div[2]/div[2]/section/div/div/div[2]/address/div/div/a[3]/text()'
        ).get()
        item["street"] = response.xpath(
            '//*[@id="frontend-offer-card"]/div[2]/div[2]/section/div/div/div[2]/address/div/div/a[4]/text()'
        ).get()
        item["house"] = response.xpath(
            '//*[@id="frontend-offer-card"]/div[2]/div[2]/section/div/div/div[2]/address/div/div/a[5]/text()'
        ).get()
        item["metro"] = response.xpath(
            '//*[@id="frontend-offer-card"]/div[2]/div[2]/section/div/div/div[2]/address/ul[1]/li[1]/a/text()'
        ).get()
        item["time_metro"] = response.xpath(
            '//*[@id="frontend-offer-card"]/div[2]/div[2]/section/div/div/div[2]/address/ul[1]/li[1]/span/text()'
        ).get()
        item["facilities"] = response.xpath(
            '//*[@id="frontend-offer-card"]/div[2]/div[2]/div[7]/div/div/div/div[2]/div/text()'
        ).get()
        item["facilities2"] = response.xpath(
            '//*[@id="frontend-offer-card"]/div[2]/div[3]/div/div[1]/div[1]/div[3]/div/div/div[6]/p[2]/text()'
        ).get()
        item["floor"] = response.xpath(
            '//*[@id="frontend-offer-card"]/div[2]/div[2]/div[4]/text()'
        ).get()
        return item
