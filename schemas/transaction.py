# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields, validate, post_dump
from lib import NotBlank
from lib.schema import DatetimeField, ObjectIdField
from lib.enums.transaction import TransactionIAPIStatus, TransactionOffChainStatus

from config import Config


class TransactionRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_address = fields.String(required=True, validate=NotBlank())
    page = fields.Integer(required=True, validate=validate.Range(min=1), default=1)
    page_size = fields.Integer(required=True, validate=validate.Range(min=1), default=10)


class TransactionResponseObj(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    from_chain_id = fields.Integer(required=True)
    from_chain = fields.String(required=True)
    to_chain_id = fields.Integer(required=True)
    to_chain = fields.Str(allow_none=True)
    user_address = fields.String(required=True, validate=NotBlank())
    contract_address = fields.String(required=True, validate=NotBlank())
    tx_hash = fields.String(required=True, validate=NotBlank())
    amount = fields.String(required=True)
    raw_amount = fields.String(required=True)
    stage = fields.Integer(required=True)
    status = fields.String(required=True, validate=validate.OneOf([
        TransactionOffChainStatus.IN_PROCESS,
        TransactionOffChainStatus.CLAIMED,
        TransactionOffChainStatus.FAIL,
        TransactionOffChainStatus.CLAIMABLE
    ]))
    signatures = fields.List(fields.String(), default=[], missing=[])
    created_time = DatetimeField()

class TransactionResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    page = fields.Integer()
    page_size = fields.Integer()
    num_of_page = fields.Integer()
    items = fields.List(fields.Nested(TransactionResponseObj), default=[])

class UpdateTransactionData(Schema):
    class Meta:
        unknown = EXCLUDE

    tx_hash = fields.String(required=True)
    from_chain_id = fields.Integer(required=True, validate=validate.OneOf(Config.CHAIN_IDS))
    to_chain_id = fields.Integer(required=True, validate=validate.OneOf(Config.CHAIN_IDS))
    status = fields.String(required=True, validate=validate.OneOf([
        TransactionIAPIStatus.FAIL,
        TransactionIAPIStatus.SUCCESS
    ]))
    node_id = fields.String(required=True)
    block_number = fields.Integer(required=True)
    signature = fields.String(required=True)