# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import logging
import sys
import traceback
from inspect import getframeinfo, stack

import sentry_sdk
from bson import json_util
from sentry_sdk import capture_exception


logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def debug(msg, *args, **kwargs):
    try:
        caller = getframeinfo(stack()[1][0])
        _msg = json_util.dumps({
            'msg': msg,
            'args': args,
            'kwargs': kwargs,
            'filename': caller.filename,
            'lineno': caller.lineno
        })
        logger.debug(_msg)
    except:
        traceback.print_exc()


class Logger(object):
    '''
    Log any message to json format.
    [TYPE] - %H:%M:%S.%f %d-%m-%Y - info
    '''

    @staticmethod
    def debug(msg, *args, **kwargs):
        try:
            caller = getframeinfo(stack()[1][0])
            _msg = json_util.dumps({
                'msg': msg,
                'args': args,
                'kwargs': kwargs,
                'filename': caller.filename,
                'lineno': caller.lineno
            })
            logger.debug(_msg)
        except:
            capture_exception()
            traceback.print_exc()


class LoggerTask(object):

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        try:
            caller = getframeinfo(stack()[1][0])
            _msg = json_util.dumps({
                'msg': msg,
                'args': args,
                'kwargs': kwargs,
                'filename': caller.filename,
                'lineno': caller.lineno
            })
            logger.debug(_msg, *args, **kwargs)

        except:
            traceback.print_exc()
            sentry_sdk.capture_exception()
