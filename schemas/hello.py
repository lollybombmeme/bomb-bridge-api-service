# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields


class HelloSchema(Schema):
    class Meta:
        unknown = RAISE

    field1 = fields.Str(required=True)
