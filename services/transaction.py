import pydash as py_
from config import Config

from helper.signature import SignatureHelper
from lib.enums.transaction import TransactionIAPIStatus, TransactionOffChainStatus
from lib.enums.transaction_verify import TransactionVerifyType
from lib.utils import dt_utcnow
from models import TransactionVerifyLogModel, TransactionsModel
from exceptions.transactions import CanNotUpdateFailedOrClaimedTransactionEx, TransactionIsFinalStageEx, TransactionNotFoundEx


class TransactionService:

    @staticmethod
    def get_user_history_transaction(params):
        user_address = py_.get(params, 'user_address').lower()
        page = py_.get(params, 'page')
        page_size = py_.get(params, 'page_size')

        return TransactionsModel.page(
            filter={
                'user_address': user_address
            },
            page=page,
            page_size=page_size,
            sort=-1,
            func_sort=lambda x: py_.get(x, 'created_time', dt_utcnow())
        )

    @staticmethod
    def get_transaction_by_tx_hash(tx_hash):
        transaction = TransactionsModel.find_one({
            'tx_hash': tx_hash
        })

        if not transaction:
            raise TransactionNotFoundEx

        return transaction

    @staticmethod
    def iapi_update_transaction(form_data):
        UPDATE_TRANSACTION_CREATED_BY = 'bomb-bridge-api:services.TransactionService:iapi_update_transaction'

        status = py_.get(form_data, 'status')
        tx_hash = py_.get(form_data, 'tx_hash')
        from_chain_id = py_.get(form_data, 'from_chain_id')
        signature = py_.get(form_data, 'signature')

        transaction = TransactionsModel.find_one({
            'tx_hash': tx_hash,
            'from_chain_id': from_chain_id
        })

        if not transaction:
            raise TransactionNotFoundEx

        if status in [TransactionOffChainStatus.FAIL, TransactionOffChainStatus.CLAIMED]:
            raise CanNotUpdateFailedOrClaimedTransactionEx

        TransactionVerifyLogModel.insert_one({
            'body': form_data,
            'current_transaction': transaction,
            'type': TransactionVerifyType.RECEIVE_VERIFY,
            'response': {},
            'created_by': UPDATE_TRANSACTION_CREATED_BY
        })

        current_stage = py_.get(transaction, 'stage')

        if current_stage >= Config.TRANSACTION_FINAL_STAGE:
            raise TransactionIsFinalStageEx

        if status == TransactionIAPIStatus.FAIL:
            TransactionsModel.update_one(
                filter={
                    'tx_hash': tx_hash,
                    'from_chain_id': from_chain_id
                },
                obj={
                    'status': TransactionOffChainStatus.FAIL,
                    'updated_by': UPDATE_TRANSACTION_CREATED_BY
                }
            )
            return {}

        update_data = {
            'updated_by': UPDATE_TRANSACTION_CREATED_BY
        }

        if current_stage + 1 >= Config.TRANSACTION_SIGN_SIGNATURE_STAGE and transaction.get("status") == TransactionOffChainStatus.IN_PROCESS:
            update_data = {
                **update_data,
                'status': TransactionOffChainStatus.CLAIMABLE
            }

        TransactionsModel.update_one(
            filter={
                'tx_hash': tx_hash,
                'from_chain_id': from_chain_id
            },
            obj=update_data,
            extract={
                '$inc': {
                    'stage': 1
                },
                '$push': {
                    "signatures": signature
                }
            }
        )

        return {}
