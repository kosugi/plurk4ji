# -*- coding: utf-8 -*-
# vim:et sts=4 sw=4

import unittest
import util

class TestUtil(unittest.TestCase):

    def setUp(self):
        self.balancer = util.Balancer()

    def test_strip_tags(self):
        self.assertEqual('', util.strip_tags(''))
        self.assertEqual('ac', util.strip_tags('a<b>c'))
        self.assertEqual('a<b', util.strip_tags('a<b'))
        self.assertEqual('a>b', util.strip_tags('a>b'))
        self.assertEqual('ace', util.strip_tags('a<b>c<d>e'))
        self.assertEqual('>ace<', util.strip_tags('>a<b>c<d>e<'))

    def t(self, xs, y):
        self.balancer.clear()
        for x in xs:
            self.balancer.read(x)
        self.assertEqual(y, self.balancer.complement())

    def test_balance(self):
        self.t([''], '')
        self.t(['a'], '')
        self.t([')'], '(')
        self.t(['('], ')')
        self.t(['(()'], '())')
        self.t(['(', '{'], '})')

if __name__ == '__main__':
    unittest.main()
