from itertools import count
import json
import re
import urllib
from html.parser import HTMLParser
from urllib.parse import urljoin

from scrapy import Field, Item, Selector
from scrapy.http import FormRequest, HtmlResponse, Request
from scrapy.spiders import CrawlSpider

from requests import Session


count = 8


class ProxyServersPro(Item):
    image = Field()
    title = Field()
    price = Field()
    brand = Field()
    store = Field()
    productID = Field()


class ProxyServers(CrawlSpider):
    name = "ProxyServersProCrawler"

    allowed_domains = [
        "hardgamers.com.ar", "www.hardgamers.com.ar"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    start_url = [
        "https://www.hardgamers.com.ar/",
    ]

    def __init__(self):
        super(ProxyServers, self).__init__()

    def start_requests(self):
        for url in self.start_url:
            yield Request(url, callback=self.parse_shops, headers=self.headers)

    def parse_shops(self, response):
        shops = response.css('.dropdown-item ::attr(href)').getall()
        shops = [k for k in shops if 'stores' in k]

        yield from response.follow_all(shops, self.parse_data)

    def parse_data(self, response):
        global count
        for post in response.css('article.product'):
            yield {
                'title': post.css('h3::text').get(),
                'brand': post.css('h4::text').get()
            }
        # yield Request('https://www.hardgamers.com.ar/stores/acuarioInsumos?page=2&limit=20&store=acuarioInsumos', callback=self.parse_data)
        next_page = response.css('a[aria-label=Next] ::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_data)
