# -*- coding: utf-8 -*-
# vim:et sts=4 sw=4

import unittest
import util

class TestUtil(unittest.TestCase):
    def setUp(self):
        self.balancer = util.Balancer()

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
