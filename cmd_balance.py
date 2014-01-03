# -*- coding: utf-8 -*-

from api import Api
from util import abort, strip_tags, Balancer
import logging

def do_post(balancer, content):
    balancer.read(strip_tags(content))

def is_god_reading_fortune(plurk):
    return 'asks' == plurk.get('qualifier') and 0 <= plurk.get('content_raw', '').find(u'神')

def do(config):

    api = Api(config['api'])
    ok, status, data = api.post('/Timeline/getUnreadPlurks')
    if not ok:
        logging.error('''api.post('/Timeline/getPlurks')''')
        logging.error('status: %s' % status)
        logging.error(data)
        return

    balancer = Balancer()
    for rec in data.get('plurks', []):
        if is_god_reading_fortune(rec):
            balancer.clear()
            plurk_id = rec.get('plurk_id', 0)
            content = rec.get('content', u'')
            do_post(balancer, content)
            logging.info('plurk: %ld' % plurk_id)
            ok, status, data = api.post('/Responses/get', dict(plurk_id=plurk_id))
            if not ok:
                logging.error('''api.post('/Responses/get', dict(plurk_id=%s))''' % plurk_id)
                logging.error('status: %s' % status)
                logging.error(data)
                return
            for rec in data.get('responses', []):
                content = rec.get('content', u'')
                do_post(balancer, content)
                logging.debug([content, balancer.complement])

            complement = balancer.complement
            if 0 < len(complement):
                logging.info('  posting: %s' % complement)
                params = dict(plurk_id=plurk_id, qualifier=':', content=complement.encode('UTF-8'))
                ok, status, data = api.post('/Responses/responseAdd', params)
                if not ok:
                    logging.error('''api.post('/Responses/responseAdd', dict(content=%s))''' % complement)
                    logging.error('status: %s' % status)
                    logging.error(data)
                    return

if __name__ == '__main__':
    import sys
    if 2 <> len(sys.argv):
        abort('usage: %s config.yml\n' % sys.argv[0])

    from config import load
    do(load(sys.argv[1]))
