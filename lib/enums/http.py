# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""


class ErrorCode(object):
    BAD_REQUEST = 'BAD_REQUEST'
    REQUIRED_AUTH = 'REQUIRED_AUTH'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    NOT_FOUND = 'NOT_FOUND'


class StatusInt(object):
    OK = 200
    BAD = 400
    NOTFOUND = 404
    FORBIDDEN = 403
    UNKNOWN = 500


class SortType:
    ASC = 'ASC'
    DESC = 'DESC'
    DEFAULT = 'DEFAULT'
