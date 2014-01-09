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

    def test_split_text(self):
        self.assertEqual(cmd_balance.split_text('', 9), [])
        self.assertEqual(cmd_balance.split_text('1', 9), ['1'])
        self.assertEqual(cmd_balance.split_text('12345678', 9),        ['12345678'])
        self.assertEqual(cmd_balance.split_text('123456789', 9),       ['1234567', '89'])
        self.assertEqual(cmd_balance.split_text('1234567890', 9),      ['1234567', '890'])
        self.assertEqual(cmd_balance.split_text('1234567890', 9),      ['1234567', '890'])
        self.assertEqual(cmd_balance.split_text('12345678901', 9),     ['1234567', '8901'])
        self.assertEqual(cmd_balance.split_text('123456789012', 9),    ['1234567', '89012'])
        self.assertEqual(cmd_balance.split_text('1234567890123', 9),   ['1234567', '890123'])
        self.assertEqual(cmd_balance.split_text('12345678901234', 9),  ['123456789', '01234'])
        self.assertEqual(cmd_balance.split_text('123456789012345', 9), ['123456789', '012345'])
        self.assertEqual(cmd_balance.split_text('1234567890123456', 9), ['1234567', '8901234', '56'])

    def test_uniquify(self):
        self.assertEqual(cmd_balance.uniquify([]), [])
        self.assertEqual(cmd_balance.uniquify(['a']), ['a'])
        self.assertEqual(cmd_balance.uniquify(['a', 'b']), ['a', 'b'])
        self.assertEqual(cmd_balance.uniquify(['a', 'a']), ['a', u'a\u200b'])
        self.assertEqual(cmd_balance.uniquify(['a', 'a', 'a']), [u'a', u'a\u200b', u'a\u200b\u200b'])
