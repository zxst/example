#coding:utf-8

import random
from scrapy import log

class RandomUserAgent(object):

    def __init__(self,agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self,request,spider):
        ua = random.choice(self.agents)
        if ua:
            print "********Current UserAgent:%s************" %ua
            request.headers.setdefault('User-Agent', random.choice(self.agents))
