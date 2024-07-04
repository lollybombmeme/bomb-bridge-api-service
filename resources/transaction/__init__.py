from resources.transaction.tx import TransactionByTxHashResource
from resources.transaction.tx_history import TransactionHistoryResource

transaction_resources = {
    '/info/<string:tx_hash>': TransactionByTxHashResource,
    '/user/': TransactionHistoryResource
}
