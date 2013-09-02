# -*- coding: utf-8 -*-

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from json import loads
from os.path import dirname, isfile, expanduser
from util import abort, obtain_latest_emos_content
import codecs

BASE = dirname(__file__) or '.'

def do(config):
    emos = loads(obtain_latest_emos_content())
    del emos['custom']

    env = Environment(loader=FileSystemLoader(BASE), extensions=['jinja2.ext.autoescape'])
    template = env.get_template('emos-template.html')
    content = template.render(emos=emos, now=datetime.now().strftime('%Y-%m-%d'))

    htmlfile = expanduser(config.get('emos_html', ''))
    try:
        with codecs.open(htmlfile, 'w', 'UTF-8') as f:
            f.write(content)
    except IOError:
        abort('bad config.emos_html: ' + htmlfile)

if __name__ == '__main__':
    import sys
    if 2 <> len(sys.argv):
        abort('usage: %s config.yml\n' % sys.argv[0])

    from config import load
    do(load(sys.argv[1]))
