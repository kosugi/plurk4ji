# -*- coding: utf-8 -*-

import oauth2 as oauth
import urlparse
import urllib
from util import abort

REQUEST_TOKEN_URL = 'http://www.plurk.com/OAuth/request_token'
ACCESS_TOKEN_URL = 'http://www.plurk.com/OAuth/access_token'
AUTHORIZE_URL = 'http://www.plurk.com/OAuth/authorize'

def do(config):
    key = config['consumer_key']
    sec = config['consumer_sec']
    consumer = oauth.Consumer(key, sec)
    c = oauth.Client(consumer)

    params = dict(
        oauth_signature_method='HMAC-SHA1',
        oauth_nonce=oauth.generate_nonce(),
        oauth_timestamp=oauth.generate_timestamp())

    req = oauth.Request.from_consumer_and_token(
        consumer=consumer,
        http_method='POST',
        http_url=REQUEST_TOKEN_URL,
        parameters=params,
        is_form_encoded=True)

    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, None)
    res = c.request(REQUEST_TOKEN_URL, method='POST', headers=req.to_header())
    r = urlparse.parse_qs(res[1])
    print r

    rt = oauth.Token(r['oauth_token'][0], r['oauth_token_secret'][0])
    print AUTHORIZE_URL + '?oauth_token=' + urllib.quote(rt.key)
    v = raw_input("PIN: ")

    params = dict(
        oauth_signature_method='HMAC-SHA1',
        oauth_nonce=oauth.generate_nonce(),
        oauth_timestamp=oauth.generate_timestamp(),
        oauth_token=rt.key,
        oauth_token_secret=rt.secret,
        oauth_verifier=v)

    req = oauth.Request.from_consumer_and_token(
        consumer=consumer,
        token=rt,
        http_method='POST',
        http_url=ACCESS_TOKEN_URL,
        parameters=params,
        is_form_encoded=True)

    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, rt)
    res = c.request(ACCESS_TOKEN_URL, method='POST', headers=req.to_header())
    r = urlparse.parse_qs(res[1])

    print "  key: '%s'" % r['oauth_token'][0]
    print "  sec: '%s'" % r['oauth_token_secret'][0]

if __name__ == '__main__':
    import sys
    if 2 <> len(sys.argv):
        abort('usage: %s config.yml\n' % sys.argv[0])

    from config import load
    do(load(sys.argv[1])['api'])
