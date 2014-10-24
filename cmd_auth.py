# -*- coding: utf-8 -*-

from oauth2 import Token, Consumer, Client
from util import abort
import urlparse
import logging

REQUEST_TOKEN_URL = 'https://www.plurk.com/OAuth/request_token'
AUTHORIZE_URL     = 'https://www.plurk.com/OAuth/authorize'
ACCESS_TOKEN_URL  = 'https://www.plurk.com/OAuth/access_token'

def do(config, token=None, sec=None, verifier=None):
    consumer = Consumer(config['consumer_key'], config['consumer_sec'])
    client = Client(consumer)
    response, content = client.request(REQUEST_TOKEN_URL, 'GET')
    request_token = dict(urlparse.parse_qsl(content))
    print request_token['oauth_token']
    print request_token['oauth_token_secret']
    print '%s?oauth_token=%s' % (AUTHORIZE_URL, request_token['oauth_token'])

def get_access_token(config, token, sec, verifier):
    consumer = Consumer(config['consumer_key'], config['consumer_sec'])
    token = Token(token, sec)
    token.set_verifier(verifier)
    client = Client(consumer, token)
    response, content = client.request(ACCESS_TOKEN_URL)
    access_token = dict(urlparse.parse_qsl(content))
    print access_token

if __name__ == '__main__':
    import sys
    from config import load

    config = load(sys.argv[1])['api']
    num_args = len(sys.argv)

    if num_args == 2:
        do(config)
    elif 2 < num_args:
        get_access_token(config, sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        abort('usage: %s config.yml\n' % sys.argv[0])
