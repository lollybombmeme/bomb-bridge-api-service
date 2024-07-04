# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import asyncio
import json

import motor
from flask_pymongo import PyMongo
import motor.motor_asyncio
from web3 import Web3
from redis import Redis
from lib import HTTPSecurity
from config import Config


class InterfaceAsync:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI)
        self.client.get_io_loop = asyncio.get_event_loop
        self.db = self.client.core


connect_db = PyMongo()
redis_standalone = Redis.from_url(Config.REDIS_URL)
security = HTTPSecurity(redis=redis_standalone)

web3_eth = Web3(Web3.HTTPProvider(
    Config.HTTP_ETH_RPC, request_kwargs={'timeout': 60}))
web3_bnb = Web3(Web3.HTTPProvider(
    Config.HTTP_BNB_RPC, request_kwargs={'timeout': 60}))

with open('lib/abi/BridgePool.json') as file:
    _bridge_pool_abi = json.load(file)
    file.close()

bridge_pool_eth = web3_eth.eth.contract(
    address=Web3.to_checksum_address(Config.BRIDGE_POOL_ETH_ADDRESS.lower()), abi=_bridge_pool_abi)

with open('lib/abi/Token.json') as file:
    _erc20_abi = json.load(file)
    file.close()

token_eth = web3_eth.eth.contract(
    address=Web3.to_checksum_address(Config.TOKEN_ETH_ADDRESS.lower()), abi=_erc20_abi)
token_bnb = web3_eth.eth.contract(
    address=Web3.to_checksum_address(Config.TOKEN_BNB_ADDRESS.lower()), abi=_erc20_abi)
