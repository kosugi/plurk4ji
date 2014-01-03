# -*- coding: utf-8 -*-
# vim:et sts=4 sw=4

import unittest
import cmd_diff_emos

class ApiMock(object):
    def __init__(self, config):
        pass

    def post(self, url, params):
        return True, 200, {}

class PasteMock(object):
    def __call__(self, desc):
        self.desc = desc
        return u''

class TestCmdDiffEmos(unittest.TestCase):

    def test_do_post(self):
        pasteMock = PasteMock()
        cmd_diff_emos.paste = pasteMock
        cmd_diff_emos.Api = ApiMock
        cmd_diff_emos.do_post(dict(api=0), set(["9", "14", "3"]), set(["8", "29", "4"]))
        self.assertEqual(u'''14\n3\n9\nが増えました\n(カルマの状態によっては使えない場合があります)\n\n29\n4\n8\nが減りました\n\n''', pasteMock.desc)

if __name__ == '__main__':
    unittest.main()
