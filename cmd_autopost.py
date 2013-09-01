# -*- coding: utf-8 -*-

from api import Api
from util import abort
import logging

def do(config):

    api = Api(config['api'])
    ok, status, data = api.post('/Profile/getOwnProfile')
    text = config['format'] % data['user_info']
    params = dict(content=text.encode('UTF-8'), qualifier=':')
    ok, status, data = api.post('/Timeline/plurkAdd', params)
    if not ok:
        logging.error('status: %s' % status)
        logging.error(data)

if __name__ == '__main__':
    import sys
    if 2 <> len(sys.argv):
        abort('usage: %s config.yml\n' % sys.argv[0])

    from config import load
    do(load(sys.argv[1]))
