# -*- coding: utf-8 -*-

from api import Api
from contextlib import closing
from email.Utils import formatdate
from email.mime.text import MIMEText
from smtplib import SMTP
import sys
import urllib
import urllib2

def obtain_latest_emos_content(config):
    api = Api(config['api'])
    ok, status, data = api.post('/Emoticons/get')
    return data

def abort(msg):
    sys.stderr.write(msg)
    sys.stderr.write('\n')
    sys.exit(1)

#
# config:
#   from: sender
#   to: recipient
#   host:
#   port:
#   username:
#   password:
#   use_tls: optional
#
def send_mail(config, subject, body):
    msg = MIMEText(body, 'plain', 'UTF-8')
    msg['From'] = config['from']
    msg['To']   = config['to']
    msg['Subject'] = subject
    msg['Date'] = formatdate()

    with closing(SMTP(config['host'], config['port'])) as smtp:
        if config['use_tls']:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
        smtp.login(config['username'], config['password'])
        smtp.sendmail(config['from'], [config['to']], msg.as_string())

# language:
#   apache: Apache Config (.htaccess)
#   bash: Bash
#   bat: Batch (.bat)
#   boo: Boo
#   c: C
#   clojure: Clojure
#   control: Debian control-files
#   cpp: C++
#   creole: Creole Wiki
#   csharp: C#
#   css: CSS
#   csv: CSV
#   d: D
#   diff: Unified Diff
#   dylan: Dylan
#   erlang: Erlang
#   gas: GAS
#   gcc-messages: GCC Messages
#   gettext: Gettext catalogs
#   haskell: Haskell
#   html+django: Django / Jinja Templates
#   html+genshi: Genshi Templates
#   html+mako: Mako Templates
#   html+myghty: Myghty Templates
#   html+php: PHP
#   html: HTML
#   ini: INI File
#   io: IO
#   irb: Interactive Ruby
#   irc: IRC Logs
#   java: Java
#   javac-messages: javac Messages
#   js: JavaScript
#   jsp: JSP
#   lighttpd: Lighttpd
#   literate-haskell: Literate Haskell
#   llvm: LLVM
#   lua: Lua
#   matlab: Matlab
#   matlabsession: Matlab Session
#   minid: MiniD
#   multi: Multi-File
#   mysql: MySQL
#   nasm: Nasm
#   nginx: Nginx
#   objectpascal: Object-Pascal
#   ocaml: OCaml
#   perl: Perl
#   php: PHP (inline)
#   povray: Povray
#   pycon: Python Console Sessions
#   pytb: Python Tracebacks
#   python: Python
#   rhtml: eRuby / rhtml
#   rst: reStructuredText
#   ruby: Ruby
#   scala: Scala
#   scheme: Scheme
#   smalltalk: Smalltalk
#   smarty: Smarty
#   sourceslist: sources.list
#   sql: SQL
#   squidconf: SquidConf
#   tex: TeX / LaTeX
#   text: Text
#   textpre: Text (preformatted)
#   vim: Vim
#   xml: XML
#   xslt: XSLT
#   yaml: YAML
#
def paste(text, language='text'):
    postdata = dict(code=text.encode('UTF-8'), language=language.encode('UTF-8'))
    with closing(urllib2.urlopen('http://paste.plurk.com/', urllib.urlencode(postdata))) as res:
        return res.geturl()

class Balancer(object):

    def __init__(self, s=None):
        if s is None:
            s = u'(){}[]<>（）〔〕［］｛｝〈〉《》「」『』【】＜＞≪≫≦≧∈∋⊆⊇⊂⊃'
        if len(s) % 2:
            raise Exception('length of the first parameter of constructor should be even.')

        self.pair_map = {}
        try:
            i = iter(s)
            while True:
                lhs = i.next()
                rhs = i.next()
                self.pair_map[lhs] = rhs
                self.pair_map[rhs] = lhs
        except StopIteration:
            pass

        self.clear()

    def clear(self):
        self.c = u''

    def read(self, s):
        for c in s:
            self.c += self.pair_map.get(c) or u''

    def complement(self):
        return self.c[::-1]
