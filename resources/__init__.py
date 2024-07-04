# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.health_check import HealthCheck
from resources.hello import HelloWorld
from resources.iapi import iapi_resources
from resources.transaction import transaction_resources

api_resources = {
    '/hello': HelloWorld,
    '/common/health_check': HealthCheck,
    **{f'/iapi{k}': val for k, val in iapi_resources.items()},
    **{f'/transaction{k}': val for k, val in transaction_resources.items()}
}
