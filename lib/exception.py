# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""


class BadRequest(Exception):
    def __init__(self, msg='Something wrong.', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_BAD_REQUEST'


class Forbidden(Exception):
    def __init__(self, msg='Forbidden', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 403
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_FORBIDDEN'


class NotFound(Exception):
    def __init__(self, msg='Not found', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 404
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_NOT_FOUND'
