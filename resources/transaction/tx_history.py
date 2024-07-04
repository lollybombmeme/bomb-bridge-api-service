# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security
from schemas.transaction import TransactionRequestSchema, TransactionResponseSchema
from services.transaction import TransactionService


class TransactionHistoryResource(Resource):

    @security.http(
        login_required=False,
        params=TransactionRequestSchema(),
        response=TransactionResponseSchema()
    )
    def get(self, params):
        _result = TransactionService.get_user_history_transaction(
            params=params)
        return _result
