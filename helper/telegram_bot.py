import requests

import pydash as py_

from config import Config


class TelegramBotHelper(object):
    @staticmethod
    def send_message(bot_message, group_id = None):
        bot_token = Config.TELEGRAM_BOT_TOKEN
        bot_chat_id = group_id if group_id else Config.TELEGRAM_GROUP_ID 
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=HTML&text=' + bot_message

        response = requests.get(send_text)

        return response.json()
