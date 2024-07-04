# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import traceback
from web3 import Web3
import pydash as py_

import sentry_sdk
from config import Config
from helper.telegram_bot import TelegramBotHelper

from worker import worker
from connect import bridge_pool_eth, token_bnb, token_eth
from tasks.telegram import send_telegram_message


# NOTE: rate is 19/s because limit of telegram rate
@worker.task(name="worker.notify_pool", rate_limit='1000/s')
def notify_pool():
    try:
        pool_balance = bridge_pool_eth.functions.balance().call()
        bnb_token_supply = token_bnb.functions.totalSupply().call()
        eth_token_supply = token_eth.functions.totalSupply().call()

        pool_balance = Web3.fromWei(pool_balance, 'ether')
        token_total_supply = Web3.fromWei(token_total_supply, 'ether')

        _message = f'<b>Pool Notify</b>\n\
            \n- Bridge Pool: {pool_balance}\
            \n- Token BNB Supply: {bnb_token_supply}\
            \n- Token ETH Supply: {eth_token_supply}\
        '

        send_telegram_message.delay(
            message=_message, group_id=Config.TELEGRAM_POOL_GROUP_ID)

        return 'DONE - send_telegram_message:'
    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return "FAIL - send_telegram_message"
