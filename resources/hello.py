# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
from flask_restful import Resource

from schemas.hello import HelloSchema
from connect import security
from tasks.bridge import on_bridge_token, on_claim_token
from connect import redis_standalone


class HelloWorld(Resource):

    @security.http()
    def get(self):
        return {'hello': 'get'}

    @security.http(
        form_data=HelloSchema(),  # form_data
        params=HelloSchema(),  # params
        login_required=True  # user
    )
    def post(self, form_data, params, user):
        return {'hello': 'post'}
