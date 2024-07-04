# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json

erc20_abi = None
with open("blockchain/abi/data/IERC20.json") as file:
    erc20_abi = json.load(file)  # load contract info as JSON

