# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

import logging
import os
import time

from scrapy.http import Request
from scrapy.item import Item
from scrapy.utils.request import request_fingerprint
from scrapy.utils.project import data_path
from scrapy.utils.python import to_bytes
from scrapy.exceptions import NotConfigured, IgnoreRequest
from scrapy import signals

import sqlite3


class HardgamersSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class IgnoreDuplicates():

    def __init__(self):
        self.crawled_urls = []

        self.con = sqlite3.connect('crawled.db')
        self.cur = self.con.cursor()

        # Drop table
        # self.cur.execute("DROP TABLE IF EXISTS crawled")

        # Create table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS crawled
                    (url text)''')

        data = self.cur.execute('''SELECT url FROM crawled''')
        self.crawled_urls = data.fetchall()

    def process_request(self, request, spider):
        url = (request.url,)
        permitted = [('https://www.hardgamers.com.ar/robots.txt',), ('https://www.hardgamers.com.ar/',), ('https://www.hardgamers.com.ar/stores/acuarioInsumos',), ('https://www.hardgamers.com.ar/stores/xtpc',), ('https://www.hardgamers.com.ar/stores/wiztech',), ('https://www.hardgamers.com.ar/stores/venex',), ('https://www.hardgamers.com.ar/stores/uranoStream',), ('https://www.hardgamers.com.ar/stores/spaceVideojuegos',), ('https://www.hardgamers.com.ar/stores/smarts',), ('https://www.hardgamers.com.ar/stores/slotOne',), ('https://www.hardgamers.com.ar/stores/scpHardStore',), ('https://www.hardgamers.com.ar/stores/peak',), ('https://www.hardgamers.com.ar/stores/nextGames',), ('https://www.hardgamers.com.ar/stores/mexx',), ('https://www.hardgamers.com.ar/stores/megasoft',), ('https://www.hardgamers.com.ar/stores/maximus',), ('https://www.hardgamers.com.ar/stores/maxTecno',), ('https://www.hardgamers.com.ar/stores/malditoHard',), ('https://www.hardgamers.com.ar/stores/liontech',), ('https://www.hardgamers.com.ar/stores/acuarioInsumos?page=2&limit=20&store=acuarioInsumos',),]
        if url in permitted:
            return None
        if url in self.crawled_urls:
            print('Request ignorado (Ya crawleado)', request.url)
            raise IgnoreRequest()
        else:
            return None

    def process_response(self, request, response, spider):
        if response.status == 200:
            print('[200] Request permitido', request.url)
            self.crawled_urls.append(request.url)
            self.cur.execute("INSERT INTO crawled VALUES(?)", (request.url,))
            self.con.commit()
            return response
        else:
            print('[%s] Request ignorado (Error)' % response.status, request.url)
            raise IgnoreRequest()
        
class HardgamersDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
