# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security
from schemas.transaction import UpdateTransactionData
from services.transaction import TransactionService


class IAPITransactionResource(Resource):

    @security.http(
        login_required=False,
        form_data=UpdateTransactionData(),
    )
    def put(self, form_data):
        _result = TransactionService.iapi_update_transaction(form_data=form_data)
        return _result
