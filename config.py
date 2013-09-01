# -*- coding: utf-8 -*-

import os
import yaml

def load(filename):
    with open(os.path.expanduser(filename), 'r') as f:
        return yaml.safe_load(f.read())
