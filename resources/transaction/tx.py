# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security
from schemas.transaction import TransactionResponseObj
from services.transaction import TransactionService


class TransactionByTxHashResource(Resource):

    @security.http(
        login_required=False,
        response=TransactionResponseObj()
    )
    def get(self, tx_hash):
        _result = TransactionService.get_transaction_by_tx_hash(tx_hash=tx_hash)
        return _result
