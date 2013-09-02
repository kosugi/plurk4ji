# -*- coding: utf-8 -*-

from api import Api
from contextlib import closing
from datetime import datetime
from functools import reduce
from json import loads
from operator import add
from os.path import isdir, expanduser
from util import abort, send_mail, paste, obtain_latest_emos_content
import codecs
import os
import urllib2

PREV_FILENAME = 'prev.json'

def extract_emo_keys(json):
    return set([x for x, y in reduce(add, json['karma'].values(), [])])

def load_saved_content(log_dir):
    try:
        with codecs.open(log_dir + '/' + PREV_FILENAME, 'r', 'UTF-8') as f:
            return f.read()
    except IOError:
        pass

def save_content(log_dir, content):
    for name in (PREV_FILENAME, datetime.now().strftime('%Y%m%d-%H%M.json')):
        with codecs.open(log_dir + '/' + name, 'w', 'UTF-8') as f:
            f.write(content)

def do_post(config, added, deled):
    api = Api(config['api'])
    desc = u''
    if added:
        desc += u'\n'.join(added) + u'\nが増えました\n(カルマの状態によっては使えない場合があります)\n\n'
    if deled:
        desc += u'\n'.join(deled) + u'\nが減りました\n\n'
    if desc:
        url = paste(desc)
        text = u' '.join([u' '.join(added), u':', url, u'(details...)'])
        params = dict(content=text.encode('UTF-8'), qualifier=':')
        ok, status, data = api.post('/Timeline/plurkAdd', params)
        if not ok:
            logging.error('status: %s' % status)
            logging.error(data)

def do(config):
    log_dir = expanduser(config.get('log_dir', ''))
    if not (isdir(log_dir) and os.access(log_dir, os.W_OK)):
        abort('bad config.log_dir: ' + log_dir)

    content_curr = obtain_latest_emos_content()
    content_prev = load_saved_content(log_dir)
    if not content_prev:
        save_content(log_dir, content_curr)
        return

    emos_curr = extract_emo_keys(loads(content_curr))
    emos_prev = extract_emo_keys(loads(content_prev))

    added = emos_curr - emos_prev
    deled = emos_prev - emos_curr
    if added or deled:
        print 'added:', added
        print 'deled:', deled
        do_post(config, added, deled)
        save_content(log_dir, content_curr)

if __name__ == '__main__':
    import sys
    if 2 <> len(sys.argv):
        abort('usage: %s config.yml\n' % sys.argv[0])

    from config import load
    do(load(sys.argv[1]))
