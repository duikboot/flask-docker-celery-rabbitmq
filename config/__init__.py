import logging
import os
import sys

import config.settings

LOGGER = logging.getLogger()

# create settings object corresponding to specified env
APP_ENV = os.environ.get('APP_ENV', 'Dev')
_current = getattr(sys.modules['config.settings'], '{0}Config'.format(APP_ENV))()

# copy attributes to the module for convenience

for attr in [f for f in dir(_current) if '__' not in f]:
    # environment can override anything
    val = os.environ.get(attr, getattr(_current, attr))
    setattr(sys.modules[__name__], attr, val)


def as_dict():
    res = {}

    for attr in [f for f in dir(config) if '__' not in f]:
        val = getattr(config, attr)
        res[attr] = val

    return res
