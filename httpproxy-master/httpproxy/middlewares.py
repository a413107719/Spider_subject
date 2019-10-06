# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
from collections import defaultdict
from random import random

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured


class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    def __init__(self, auth_encoding='latin-1', proxy_list_file=None):
        super().__init__(auth_encoding)
        if not proxy_list_file:
            raise NotConfigured

        self.auth_encoding = auth_encoding
        self.proxies = defaultdict(list)

        with open(proxy_list_file) as f:
            proxy_list = json.load(f)
            for proxy in proxy_list:
                scheme = proxy['proxy_scheme']
                url = proxy['proxy']

        self.proxies[scheme].append(self._get_proxy(url, scheme))

        @classmethod
        def from_crawler(cls, crawler):
            auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'lantain-1')

            proxy_list_file = crawler.settings.get('HTTPPROXY_PROXY_LIST_FILE')

            return cls(auth_encoding, proxy_list_file)

        def _set_proxy(self, request, scheme):
            creds,proxy = random.choice(self.proxies[scheme])
            request.meta['proxy'] = proxy
            if creds:
                request.headers['Proxy-Authorization'] = b'Basic' + creds