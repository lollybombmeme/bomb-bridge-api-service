# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
__models__ = ['SignaturesModel']

from config import Config
from connect import connect_db, redis_standalone
from lib import DaoModel

SignaturesModel = DaoModel(
    col=connect_db.db.signatures, redis=redis_standalone)
TransactionsModel = DaoModel(
    col=connect_db.db.transactions, redis=redis_standalone)
TransactionVerifyLogModel = DaoModel(
    col=connect_db.db.transaction_verify_logs, redis=redis_standalone)
TxLogsModel = DaoModel(col=connect_db.db.tx_logs, redis=redis_standalone)
