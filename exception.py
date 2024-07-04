# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""


class TxRecorded(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 300
        self.msg = 'This tx has been recorded. Please see the results in your transaction history.'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_TX_RECORDED'

    pass


class TxPayment(Exception):
    def __init__(self, msg="Order not found in payment queue.", *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_PAYMENT'

    pass


class TxTimeout(Exception):
    def __init__(self, msg="The payment period for the order has expired.", *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_PAYMENT_TIMEOUT'

    pass


class ExPromoCodeInvalid(Exception):
    def __init__(self, msg="Promo code out of used or does not exist.", *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_PROMO_CODE'

    pass


class ExRefCodeInvalid(Exception):
    def __init__(self, msg="Referral code does not exist.", *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_REFERRAL_CODE'

    pass


class ExRefCodeOwner(Exception):
    def __init__(self, msg="Can not use owner referral code.", *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_REFERRAL_CODE'

    pass


class ExCheckFiat(Exception):
    def __init__(self, msg="Simplex error.", *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 401
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_FAIT'

    pass
