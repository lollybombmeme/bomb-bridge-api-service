class TransactionNotFoundEx(Exception):
    def __init__(self, msg='Transaction Not Found', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_TRANSACTION_NOT_FOUND'

class TransactionInConfirmEx(Exception):
    def __init__(self, msg='Transaction In Confirm', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_TRANSACTION_IN_CONFIRM'

class TransactionCanNotClaimEx(Exception):
    def __init__(self, msg='Transaction Can Not Claim', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_TRANSACTION_CAN_NOT_CLAIM'

class TransactionChainIdNotSameEx(Exception):
    def __init__(self, msg='Transaction Chain Id Not Same', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_TRANSACTION_CHAIN_ID_NOT_SAME'

class TransactionUserAddressNotSameEx(Exception):
    def __init__(self, msg='Transaction User Address Not Same', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_TRANSACTION_USER_ADDRESS_NOT_SAME'

class TransactionIsFinalStageEx(Exception):
    def __init__(self, msg='Transaction Is Final Stage', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_TRANSACTION_FINAL_STAGE'

class CanNotUpdateFailedOrClaimedTransactionEx(Exception):
    def __init__(self, msg='Can Not Update Failed Or Claimed Transaction', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_CAN_NOT_UPDATE_FAILED_OR_CLAIMED_TRANSACTION'
