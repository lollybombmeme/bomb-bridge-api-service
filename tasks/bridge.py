import traceback
import web3

import requests
import sentry_sdk
from bson import ObjectId
import bson.json_util
import pydash as py_
from decimal import Decimal

from config import Config
from lib.enums.transaction import TransactionOffChainStatus
from lib.enums.transaction_verify import TransactionVerifyType
from lib.logger import debug
from lib.utils import dt_utcnow
from tasks.notify_pool import notify_pool
from tasks.telegram import send_telegram_message
from worker import worker
from connect import redis_standalone
from models import TransactionVerifyLogModel, TransactionsModel, TxLogsModel
from lib import LockTaskHelper
from lib.enum import CHAIN_MAPPING

LOCK_BRIDGE_TX_HASH_KEY = 'bomb.bridge-api:bridge:lock'
LOCK_CLAIM_TX_HASH_KEY = 'bomb.bridge-api:claim:lock'


LockBridgeTask = LockTaskHelper(
    lock_key=LOCK_BRIDGE_TX_HASH_KEY, redis=redis_standalone)
LockClaimTask = LockTaskHelper(
    lock_key=LOCK_CLAIM_TX_HASH_KEY, redis=redis_standalone)


@worker.task(name="worker.on_bridge_token", rate_limit="1000/s", bind=True, max_retries=3)
def on_bridge_token(self, event):
    _tx_hash = py_.get(event, 'transactionHash')
    # NOTE: tx_hash is callback data for claim token on bridge chain
    try:

        _user_address = py_.get(event, 'args.wallet').lower()
        _amount = py_.get(event, 'args.amount')
        _to_chain_id = py_.to_integer(py_.get(event, 'args.toChainId'))
        _from_chain_id = py_.to_integer(py_.get(event, 'chain'))
        _contract_address = py_.get(event, 'address').lower()
        _block_number = py_.get(event, 'blockNumber')

        if _to_chain_id not in Config.CHAIN_IDS:
            return f'FAIL - not support this chain_id: {_to_chain_id}, {event}'

        _is_lock = LockBridgeTask.is_lock(
            key_suffix=f'{_from_chain_id}:{_tx_hash}')

        if _is_lock:
            return f'FAIL - tx_hash in process: {event}'

        _tx = TxLogsModel.find_one({
            'tx_hash': _tx_hash,
            'chain_id': _from_chain_id,
        })

        if _tx:
            return f'FAIL - tx_hash has been processed'

        _amount_from_wei = str(web3.Web3.from_wei(
            int(Decimal(_amount)), 'ether'))

        _update_data = {
            'tx_hash': _tx_hash,
            'user_address': _user_address,
            'contract_address': _contract_address,
            'from_chain_id': _from_chain_id,
            'from_chain': py_.get(CHAIN_MAPPING, py_.to_string(_from_chain_id)),
            'to_chain_id': _to_chain_id,
            'to_chain': py_.get(CHAIN_MAPPING, py_.to_string(_to_chain_id)),
            'amount': _amount_from_wei,
            'raw_amount': _amount,
            'stage': 0,
            'signatures': [],
            'status': TransactionOffChainStatus.IN_PROCESS,
            'created_time': dt_utcnow(),
            'updated_by': 'bomb-bridge-api.tasks:on_bridge_token'
        }

        TransactionsModel.update_one({
            'tx_hash': _tx_hash,
            'from_chain_id': _from_chain_id
        }, _update_data, upsert=True)

        _url = f'{Config.GUARD_API_URL}/iapi/evident'

        _body = {
            "contract_address": web3.Web3.to_checksum_address(_contract_address),
            "user_address": web3.Web3.to_checksum_address(_user_address),
            "amount": py_.to_string(_amount),
            "tx_hash": _tx_hash,
            "from_chain_id": _from_chain_id,
            "to_chain_id": _to_chain_id,
        }

        _res = requests.post(_url, json=_body)
        print(_res.status_code, _res.json())

        TransactionVerifyLogModel.insert_one({
            'body': _body,
            'type': TransactionVerifyType.CALL_VERIFY,
            'current_transaction': {
                **_update_data,
                'tx_hash': _tx_hash,
                'contract_address': _contract_address
            },
            'response': _res.json(),
            'created_by': 'bomb-bridge-api.tasks:on_bridge_token'
        })

        if _res.status_code != 200:
            raise Exception('Send event to guard-api fail')

        TxLogsModel.insert_one({
            'contract': _contract_address,
            'tx_hash': _tx_hash,
            'event': bson.json_util.dumps(event),
            'block_number': _block_number,
            'tx_type': 'Bridge',
            'chain_id': _from_chain_id,
            'created_by': 'bomb-bridge-api.tasks:on_bridge_token'
        })

        _message = f'<b>New User Bridge</b>\n\
                \n- User Address: {_user_address}\
                \n- From Chain: {py_.get(CHAIN_MAPPING, py_.to_string(_from_chain_id))}\
                \n- To Chain: {py_.get(CHAIN_MAPPING, py_.to_string(_to_chain_id))}\
                \n- Tx Hash: {_tx_hash}\
                \n- Amount: {_amount_from_wei}\
            '

        send_telegram_message.delay(message=_message)

        LockBridgeTask.lock(key_suffix=_tx_hash)

        return f'DONE - on_bridge_token: {event}'

    except Exception as e:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        LockBridgeTask.unlock(key_suffix=_tx_hash)
        # NOTE: retry task if has error after 5 seconds
        self.retry(exc=e, countdown=10)
        return 'FAIL'


@worker.task(name="worker.on_claim_token", rate_limit="1000/s", bind=True, max_retries=3)
def on_claim_token(self, event):
    # NOTE: tx_hash is callback data for claim token on bridge chain
    _transaction_hash = py_.get(event, 'transactionHash')
    try:

        _tx_hash = py_.get(event, 'args.callbackData')
        _from_chain_id = py_.to_integer(py_.get(event, 'chain'))
        _contract_address = py_.get(event, 'address').lower()
        _block_number = py_.get(event, 'blockNumber')

        _transaction = TransactionsModel.find_one({
            'tx_hash': _tx_hash
        })

        if not _transaction:
            return f'FAIL - transaction not found: {event}'

        _transaction_status = py_.get(_transaction, 'status')
        if _transaction_status != TransactionOffChainStatus.CLAIMABLE:
            return f'FAIL - transaction is not claimable: {event}'

        if _from_chain_id not in Config.CHAIN_IDS:
            return f'FAIL - not support this chain_id: {_from_chain_id}, {event}'

        _is_lock = LockClaimTask.is_lock(
            key_suffix=f'{_from_chain_id}:{_transaction_hash}')

        if _is_lock:
            return f'FAIL - tx_hash in process: {event}'

        TransactionsModel.update_one({
            'tx_hash': _tx_hash,
            'from_chain_id': py_.get(_transaction, 'from_chain_id')
        }, {
            'status': TransactionOffChainStatus.CLAIMED,
            'updated_by': 'bomb-bridge-api.tasks:on_bridge_token'
        })

        TxLogsModel.insert_one({
            'contract': _contract_address,
            'tx_hash': _transaction_hash,
            'event': bson.json_util.dumps(event),
            'block_number': _block_number,
            'tx_type': 'Claim',
            'chain_id': _from_chain_id,
            'created_by': 'bomb-bridge-api.tasks:on_bridge_token'
        })

        _message = f'<b>User Claim Success</b>\n\
            \n- User Address: {py_.get(_transaction, "user_address")}\
            \n- From Chain: {py_.get(_transaction, "from_chain")}\
            \n- To Chain: {py_.get(_transaction, "to_chain")}\
            \n- Tx Hash: {_tx_hash}\
            \n- Amount: {py_.get(_transaction, "amount")}\
        '

        send_telegram_message.delay(message=_message)
        notify_pool.delay()

        LockClaimTask.lock(key_suffix=_tx_hash)

        return f'DONE - on_bridge_token: {event}'

    except Exception as e:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        LockClaimTask.unlock(key_suffix=_transaction_hash)
        # NOTE: retry task if has error after 5 seconds
        self.retry(exc=e, countdown=10)
        return 'FAIL'
