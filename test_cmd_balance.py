# -*- coding: utf-8 -*-
# vim:et sts=4 sw=4

import unittest
import cmd_balance

class TestCmdBalance(unittest.TestCase):

    def test_is_god_reading_fortune(self):
        self.assertFalse(cmd_balance.is_god_reading_fortune(dict(qualifier=u'', content_raw=u'')))
        self.assertFalse(cmd_balance.is_god_reading_fortune(dict(qualifier=u'asks', content_raw=u'')))
        self.assertFalse(cmd_balance.is_god_reading_fortune(dict(qualifier=u'', content_raw=u'神')))
        self.assertTrue (cmd_balance.is_god_reading_fortune(dict(qualifier=u'asks', content_raw=u'神')))
        self.assertTrue (cmd_balance.is_god_reading_fortune(dict(qualifier=u'asks', content_raw=u' 神')))
        self.assertTrue (cmd_balance.is_god_reading_fortune(dict(qualifier=u'asks', content_raw=u'神 ')))
        self.assertTrue (cmd_balance.is_god_reading_fortune(dict(qualifier=u'asks', content_raw=u' 神 ')))
        self.assertTrue (cmd_balance.is_god_reading_fortune(dict(qualifier=u'asks', content_raw=u'---神 一富士二鷹三茄子---')), u'実例')
        self.assertTrue (cmd_balance.is_god_reading_fortune(dict(qualifier=u'asks', content_raw=u'神 もう一度')), u'実例')
        self.assertTrue (cmd_balance.is_god_reading_fortune(dict(qualifier=u'asks', content_raw=u'神　もう一度')), u'実例')
