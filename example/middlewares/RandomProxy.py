#coding utf-8
from example import settings

class RandomProxy(object):

    def __init__(self):
        self.author = 'zxst'

    def process_request(self,request,spider):
        request.meta['proxy'] = settings.HTTP_PROXY
