#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
import ConfigParser
import os

CONFIG_FILE = '/home/svoronov/fail.conf'
def func(conf):
    if os.access(conf, os.R_OK):
        try:
            settings = ConfigParser.ConfigParser()
            settings.read(conf)
            return settings
        except ConfigParser.Error as err:
            print err
            return None


class TestArborBlockerFuncts(unittest.TestCase):
    @mock.patch('ConfigParser.ConfigParser.read')
    @mock.patch('os.access')
    def test_load_config(self, mock_access, mock_read):
        mock_access.return_value = True
        self.assertIsInstance(func("test"), ConfigParser.ConfigParser)
        mock_read.assert_called_with("test")

if __name__ == "__main__":  # pragma: no cover
    unittest.main(verbosity=2)



