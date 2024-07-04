ethereum = {
    "id": 1,
    "network": "homestead",
    "name": "Ethereum",
    "nativeCurrency": {
        "name": "Ether",
        "symbol": "ETH",
        "decimals": 18,
    },
    "rpcUrls": {
        "alchemy": {
            "http": ["https://eth-mainnet.g.alchemy.com/v2"],
            "webSocket": ["wss://eth-mainnet.g.alchemy.com/v2"],
        },
        "infura": {
            "http": ["https://mainnet.infura.io/v3"],
            "webSocket": ["wss://mainnet.infura.io/ws/v3"],
        },
        "default": {
            "http": ["https://cloudflare-eth.com"],
        },
        "public": {
            "http": ["https://cloudflare-eth.com"],
        },
    },
    "blockExplorers": {
        "etherscan": {
            "name": "Etherscan",
            "url": "https://etherscan.io",
        },
        "default": {
            "name": "Etherscan",
            "url": "https://etherscan.io",
        },
    },
    "testnet": False,
}

goerli = {
    "id": 5,
    "network": "goerli",
    "name": "Goerli",
    "nativeCurrency": {
        "name": "Goerli Ether",
        "symbol": "ETH",
        "decimals": 18,
    },
    "rpcUrls": {
        "alchemy": {
            "http": ["https://eth-goerli.g.alchemy.com/v2"],
            "webSocket": ["wss://eth-goerli.g.alchemy.com/v2"],
        },
        "infura": {
            "http": ["https://goerli.infura.io/v3"],
            "webSocket": ["wss://goerli.infura.io/ws/v3"],
        },
        "default": {
            "http": ["https://rpc.ankr.com/eth_goerli"],
        },
        "public": {
            "http": ["https://rpc.ankr.com/eth_goerli"],
        },
    },
    "blockExplorers": {
        "etherscan": {
            "name": "Etherscan",
            "url": "https://goerli.etherscan.io",
        },
        "default": {
            "name": "Etherscan",
            "url": "https://goerli.etherscan.io",
        },
    },
    "testnet": True,
}

bsc_testnet = {
    "id": 97,
    "name": "Binance Smart Chain Testnet",
    "network": "bsc-testnet",
    "nativeCurrency": {
        "decimals": 18,
        "name": "BNB",
        "symbol": "tBNB",
    },
    "rpcUrls": {
        "default": {
            "http": ["https://bsc-testnet.public.blastapi.io"],
        },
        "public": {
            "http": ["https://bsc-testnet.public.blastapi.io"],
        },
    },
    "blockExplorers": {
        "etherscan": {
            "name": "BscScan",
            "url": "https://testnet.bscscan.com",
        },
        "default": {
            "name": "BscScan",
            "url": "https://testnet.bscscan.com",
        },
    },
    "testnet": True,
}

bsc = {
    "id": 56,
    "name": "BNB Smart Chain",
    "network": "bsc",
    "nativeCurrency": {
        "decimals": 18,
        "name": "BNB",
        "symbol": "BNB",
    },
    "rpcUrls": {
        "default": {
            "http": ["https://rpc.ankr.com/bsc"],
        },
        "public": {
            "http": ["https://rpc.ankr.com/bsc"],
        },
    },
    "blockExplorers": {
        "etherscan": {
            "name": "BscScan",
            "url": "https://bscscan.com",
        },
        "default": {
            "name": "BscScan",
            "url": "https://bscscan.com",
        },
    },
    "testnet": False,
}

zksync = {
    "id": 324,
    "name": "zkSync",
    "network": "zksync",
    "nativeCurrency": {
        "decimals": 18,
        "name": "Ether",
        "symbol": "ETH",
    },
    "rpcUrls": {
        "default": {
            "http": ["https://zksync2-mainnet.zksync.io"],
            "webSocket": ["wss://zksync2-mainnet.zksync.io/ws"],
        },
        "public": {
            "http": ["https://zksync2-mainnet.zksync.io"],
            "webSocket": ["wss://zksync2-mainnet.zksync.io/ws"],
        },
    },
    "blockExplorers": {
        "default": {
            "name": "zkExplorer",
            "url": "https://explorer.zksync.io",
        },
    },
    "testnet": False,
}

zksync_testnet = {
    "id": 280,
    "name": "zkSync Testnet",
    "network": "zksync-testnet",
    "nativeCurrency": {
        "name": "Ether",
        "symbol": "ETH",
        "decimals": 18,
    },
    "rpcUrls": {
        "default": {
            "http": ["https://zksync2-testnet.zksync.dev"],
            "webSocket": ["wss://zksync2-testnet.zksync.dev/ws"],
        },
        "public": {
            "http": ["https://zksync2-testnet.zksync.dev"],
            "webSocket": ["wss://zksync2-testnet.zksync.dev/ws"],
        },
    },
    "blockExplorers": {
        "default": {
            "name": "zkExplorer",
            "url": "https://goerli.explorer.zksync.io",
        },
    },
    "testnet": True,
}

base_testnet = {
    "id": 84531,
    "name": "Base Goerli Testnet",
    "network": "base-goerli-testnet",
    "nativeCurrency": {
        "decimals": 18,
        "name": "Base Goerli Ether",
        "symbol": "ETH",
    },
    "rpcUrls": {
        "default": {
            "http": ["https://goerli.base.org"],
        },
        "public": {
            "http": ["https://goerli.base.org"],
        },
    },
    "blockExplorers": {
        "etherscan": {
            "name": "BaseScan",
            "url": "https://goerli.basescan.org/",
        },
        "default": {
            "name": "BaseScan",
            "url": "https://goerli.basescan.org/",
        },
    },
    "testnet": True,
}

scroll = {
    "id": 534352,
    "name": "Scroll",
    "network": "scroll",
    "nativeCurrency": {
        "decimals": 18,
        "name": "Scroll Ether",
        "symbol": "ETH",
    },
    "rpcUrls": {
        "default": {
            "http": [
                "https://scroll-prealpha.blockpi.network/v1/rpc/public",
                "https://scroll-alphanet.public.blastapi.io"
            ],
        },
        "public": {
            "http": [
                "https://scroll-prealpha.blockpi.network/v1/rpc/public",
                "https://scroll-alphanet.public.blastapi.io"
            ],
        },
    },
    "blockExplorers": {
        "etherscan": {
            "name": "ScrollScan",
            "url": "https://blockscout.scroll.io/",
        },
        "default": {
            "name": "ScrollScan",
            "url": "https://blockscout.scroll.io/",
        },
    },
    "testnet": False,
}

scroll_testnet = {
    "id": 534353,
    "name": "Scroll Alpha Testnet",
    "network": "scroll-alpha-testnet",
    "nativeCurrency": {
        "decimals": 18,
        "name": "Scroll Alpha Ether",
        "symbol": "ETH",
    },
    "rpcUrls": {
        "default": {
            "http": [
                "https://scroll-prealpha.blockpi.network/v1/rpc/public",
                "https://scroll-alphanet.public.blastapi.io"
            ],
        },
        "public": {
            "http": [
                "https://scroll-prealpha.blockpi.network/v1/rpc/public",
                "https://scroll-alphanet.public.blastapi.io"
            ],
        },
    },
    "blockExplorers": {
        "etherscan": {
            "name": "ScrollScan",
            "url": "https://blockscout.scroll.io/",
        },
        "default": {
            "name": "ScrollScan",
            "url": "https://blockscout.scroll.io/",
        },
    },
    "testnet": True,
}
