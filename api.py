# -*- coding: utf-8 -*-

from json import loads
from oauth2 import Token, Consumer, Client
from urllib import urlencode
import logging
import traceback

class Api(object):

    BASE = 'https://www.plurk.com/APP'

    def __init__(self, config):
        self.consumer = Consumer(config['consumer_key'], config['consumer_sec'])
        self.token = Token(config['key'], config['sec'])

    def request(self, method, url, query=''):

        client = Client(self.consumer, self.token)
        headers, body = client.request(self.BASE + url, method=method, body=query)

        status = headers.get('status')
        json = None
        try:
            if status < '500':
                json = loads(body)
        except ValueError:
            logging.warn(traceback.format_exc())
            logging.warn(body)
        return status == '200', status, json

    def post(self, url, params=None):
        query = urlencode(params) if params is not None else ''
        return self.request('POST', url, query)

    def get(self, url, params=None):
        query = urlencode(params) if params is not None else ''
        return self.request('GET', url + '?' + query)
