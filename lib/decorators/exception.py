# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback
from functools import wraps

import sentry_sdk


def handle_exception(default=None, tracking=True, is_raise=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                if tracking:
                    sentry_sdk.capture_exception()
                    traceback.print_exc()
                if is_raise:
                    raise
                return default

        return wrapper

    return decorator
