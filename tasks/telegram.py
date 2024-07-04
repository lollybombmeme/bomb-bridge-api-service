# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback

import sentry_sdk
from helper.telegram_bot import TelegramBotHelper

from worker import worker


#NOTE: rate is 19/s because limit of telegram rate
@worker.task(name="worker.send_telegram_message", rate_limit='29/s')
def send_telegram_message(message, group_id=None):
    try:
        TelegramBotHelper.send_message(bot_message=message, group_id=group_id)
        return f'DONE - send_telegram_message: {message}'
    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return "FAIL - send_telegram_message"
