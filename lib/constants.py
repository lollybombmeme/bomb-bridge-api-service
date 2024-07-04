# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from .chains import ethereum, goerli, bsc, bsc_testnet, zksync, zksync_testnet, base_testnet, scroll, scroll_testnet

PAGE_SIZE_DEFAULT = 10

CHAIN_BY_IDS = {
    1: ethereum,
    5: goerli,
    56: bsc,
    97: bsc_testnet,
    324: zksync,
    280: zksync_testnet,
    84531: base_testnet,
    534352: scroll,
    534353: scroll_testnet,
}
