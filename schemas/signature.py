# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate
from lib import NotBlank

from config import Config


class SignatureRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    chain_id = fields.Integer(
        required=True, validate=validate.OneOf(Config.CHAIN_IDS))
    user_address = fields.String(required=True, validate=NotBlank())
    contract_address = fields.String(required=True, validate=NotBlank())
    tx_hash = fields.String(required=True, validate=NotBlank())


class SignatureDataObj(SignatureRequestSchema):
    class Meta:
        unknown = EXCLUDE

    amount = fields.String(required=True)


class SignatureResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    signature = fields.String(required=True, validate=NotBlank())
    deadline = fields.Integer(required=True)
    data = fields.Nested(SignatureDataObj, required=True)
