# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("DEBUG")
    PROJECT = "bomb-bridge"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SENTRY_DSN = os.getenv('SENTRY_DSN')

    # Setup db
    MONGO_URI = os.getenv('MONGO_URI')

    # Authentication
    TOKEN_EXPIRE_TIME = int(os.getenv('TOKEN_EXP_TIME', default='864000'))

    # Config celery worker
    CELERY_IMPORTS = ['tasks']
    ENABLE_UTC = True

    BROKER_USE_SSL = True
    BROKER_URL = os.getenv('BROKER_URL')
    CELERY_QUEUES = os.getenv('CELERY_QUEUES')

    CELERY_ROUTES = {
        'worker.on_bridge_token': 'bomb-bridge-queue',
        'worker.on_claim_token': 'bomb-bridge-queue',
        'worker.send_telegram_message': 'bomb-bridge-queue',
        'worker.notify_pool': 'bomb-bridge-queue',
    }

    CHAIN_IDS = json.loads(os.getenv('CHAIN_IDS'))

    # SIGNATURE_SIGN_PRIVATE_KEY = os.getenv('SIGNATURE_SIGN_PRIVATE_KEY')

    # Redis
    REDIS_URL = os.getenv('REDIS_URL')
    GUARD_API_URL = os.getenv('GUARD_API_URL')

    # Bot
    TELEGRAM_GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')
    TELEGRAM_POOL_GROUP_ID = os.getenv('TELEGRAM_POOL_GROUP_ID')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    # Constants Config
    BLOCKCHAIN_DECIMALS = {
        '0': 'wei',
        '3': 'kwei',
        '6': 'mwei',
        '9': 'gwei',
        '12': 'szabo',
        '15': 'finney',
        '18': 'ether'
    }
    SIGNATURE_EXPIRE_TIME = 60 * 5
    TRANSACTION_SIGN_SIGNATURE_STAGE = 3
    TRANSACTION_FINAL_STAGE = 5

    HTTP_ETH_RPC = os.getenv('HTTP_ETH_RPC')
    HTTP_BNB_RPC = os.getenv('HTTP_BNB_RPC')

    BRIDGE_POOL_ETH_ADDRESS = os.getenv('BRIDGE_POOL_ETH_ADDRESS')
    TOKEN_ETH_ADDRESS = os.getenv('TOKEN_ETH_ADDRESS')
    TOKEN_BNB_ADDRESS = os.getenv('TOKEN_BNB_ADDRESS')
