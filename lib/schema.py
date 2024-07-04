# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from __future__ import annotations

import re
import traceback
import typing

from marshmallow import Schema, fields, INCLUDE, ValidationError
from marshmallow.validate import Validator
from datetime import datetime, timezone
from bson import ObjectId

from .utils import is_oid
from .language import Language


class ObjectIdField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value and isinstance(value, str):
            return ObjectId(value)
        return value

    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "invalid": "Not a valid ObjectId",
    }

    def _deserialize(
            self,
            value,
            *args,
            **kwargs
    ):
        if isinstance(value, ObjectId):
            return str(value)
        return value


class DatetimeField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        MIN_YEAR = 1
        MAX_YEAR = 9999
        if isinstance(value, (float, int)):
            if MIN_YEAR * 365 * 86400 <= float(value) <= MAX_YEAR * 365 * 86400:
                return datetime.fromtimestamp(value, tz=timezone.utc)
        return datetime.fromtimestamp(0, tz=timezone.utc)

    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Not a valid seconds timestamp.",
    }

    def _deserialize(
            self,
            value,
            *args,
            **kwargs
    ):
        print('_deserialize', value)
        if isinstance(value, datetime):
            return value.replace(tzinfo=timezone.utc).timestamp()

        return 0


class IsObjectId(Validator):
    message_error = "It must be a 12-byte input or a 24-character hex string."

    def __init__(self):
        pass

    def _repr_args(self) -> str:
        return f""

    def _format_error(self, value: typing.Sized, message: str) -> str:
        return (self.error or message).format(
            value=value
        )

    def __call__(self, value):
        if not is_oid(value):
            raise ValidationError(self._format_error(value, self.message_error))

        return value


class NotBlank(Validator):
    message_error = "Field cannot be blank."

    def _repr_args(self) -> str:
        return ""

    def _format_error(self, value: typing.Sized, message: str) -> str:
        return (self.error or message).format(
            value=value
        )

    def __call__(self, value):
        value = " ".join(value.split())
        if not value:
            raise ValidationError(self._format_error(value, self.message_error))

        return value


class UrlField(fields.Str):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return value
        if not isinstance(value, str):
            raise self.make_error("invalid", input=value)

        if value.startswith('www.'):
            value = value.replace('www.', '', 1)
        if value.startswith('http://'):
            value = value.replace('http://', '', 1)
        if not re.match('^https://', value):
            value = f'https://{value}'

        return value

    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "invalid": "Not a valid URL."
    }

    def _deserialize(
            self,
            value,
            *args,
            **kwargs
    ):
        return value

class BaseReq(Schema):
    class Meta:
        ordered = True
        unknown = INCLUDE

    language = fields.Str(missing=Language.DEFAULT, default=Language.DEFAULT, allow_none=True)
