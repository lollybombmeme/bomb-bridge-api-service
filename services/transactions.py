import pydash as py_
from config import Config
import web3
import bson
import pymongo

from helper.signature import SignatureHelper
from lib.enums.transaction import TransactionIAPIStatus, TransactionOffChainStatus
from lib.enums.transaction_verify import TransactionVerifyType
from lib.utils import dt_utcnow
from models import TransactionVerifyLogModel, TransactionsModel
from exceptions.requests import IsNotValidObjIdEx
from exceptions.transactions import CanNotUpdateFailedOrClaimedTransactionEx, TransactionIsFinalStageEx, TransactionNotFoundEx


class TransactionService:

    @staticmethod
    def get_user_history_transaction(params):
        _user_address = py_.get(params, 'user_address').lower()
        _page = py_.get(params, 'page')
        _page_size = py_.get(params, 'page_size')

        _result = TransactionsModel.page(
            filter={
                'user_address': _user_address
            },
            page=_page,
            page_size=_page_size,
            sort=-1,
            func_sort=lambda x: py_.get(x, 'created_time', dt_utcnow())
        )

        return _result

    @staticmethod
    def get_transaction_by_tx_hash(tx_hash):
        _transaction = TransactionsModel.find_one({
            'tx_hash': tx_hash
        })

        if not _transaction:
            raise TransactionNotFoundEx
        
        return _transaction


    @staticmethod
    def iapi_update_transaction(form_data):
        _status = py_.get(form_data, 'status')
        _tx_hash = py_.get(form_data, 'tx_hash')
        _from_chain_id = py_.get(form_data, 'from_chain_id')
        _signature = py_.get(form_data, 'signature')

        _transaction = TransactionsModel.find_one({
            'tx_hash': _tx_hash,
            'from_chain_id': _from_chain_id
        })

        if not _transaction:
            raise TransactionNotFoundEx

        if py_.get(_transaction, 'status') in [TransactionOffChainStatus.FAIL, TransactionOffChainStatus.CLAIMED]:
            raise CanNotUpdateFailedOrClaimedTransactionEx
        
        TransactionVerifyLogModel.insert_one({
            'body': form_data,
            'current_transaction': _transaction,
            'type': TransactionVerifyType.RECEIVE_VERIFY,
            'response': {},
            'created_by': 'bomb-bridge-api:services.TransactionService:iapi_update_transaction'
        })

        _current_stage = py_.get(_transaction, 'stage')

        if _current_stage >= Config.TRANSACTION_FINAL_STAGE:
            raise TransactionIsFinalStageEx

        if _status == TransactionIAPIStatus.FAIL:
            TransactionsModel.update_one(
                filter={
                    'tx_hash': _tx_hash,
                    'from_chain_id': _from_chain_id
                },
                obj={
                    'status': TransactionOffChainStatus.FAIL,
                    'updated_by': 'bomb-bridge-api:services.TransactionService:iapi_update_transaction'
                }
            )

            return {}

        _update_data = {
            'updated_by': 'bomb-bridge-api:services.TransactionService:iapi_update_transaction'
        }

        if _current_stage + 1 >= Config.TRANSACTION_SIGN_SIGNATURE_STAGE and py_.get(_transaction, 'status') == TransactionOffChainStatus.IN_PROCESS:
            _update_data = {
                **_update_data,
                'status': TransactionOffChainStatus.CLAIMABLE
            }

        TransactionsModel.update_one(
            filter={
                'tx_hash': _tx_hash,
                'from_chain_id': _from_chain_id
            },
            obj=_update_data,
            extract={
                '$inc': {
                    'stage': 1
                },
                '$push': {
                    "signatures": _signature
                }
            }
        )

        return {}