# -*- coding: utf-8 -*-

import os
import yaml
import logging.config

def load(filename):
    with open(os.path.expanduser(filename), 'r') as f:
        config = yaml.load(f.read()) # SMTPHandler requires tuple
        logging.config.dictConfig(config.get('logging', dict(version=1)))
        return config
