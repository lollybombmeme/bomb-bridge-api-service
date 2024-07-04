import eth_abi
from eth_account.messages import encode_defunct
import eth_abi.abi
import web3
import pydash as py_

from config import Config
from lib import dt_utcnow


class SignatureHelper:

    @staticmethod
    def verify_signature(data):
        chain_id = py_.get(data, 'chain_id')
        user_address = py_.get(data, 'user_address')
        contract_address = py_.get(data, 'contract_address')
        tx_hash = py_.get(data, 'tx_hash')
        amount = py_.get(data, 'amount')
        signature = py_.get(data, 'signature')

        encoded_message = eth_abi.abi.encode(
            [
                'uint256',  # chain_id
                'address',  # user_address
                'address',  # contract creator
                'string',  # tx_hash
                'uint256',  # amount
            ],
            [
                chain_id,
                user_address,
                contract_address,
                tx_hash,
                amount,
            ]
        )

        message = encode_defunct(encoded_message)
        recovered_address = web3.Account.recover_message(
            message, signature=signature)

        return recovered_address in Config.NODE_VERIFY_ADDRESSES
