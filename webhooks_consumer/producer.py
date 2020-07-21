import requests

from django.conf import settings

from slackclient import SlackClient


class SlackMessageProducer:
    def __init__(self, slack_bot_token, slack_channel_name):
        self.client = SlackClient(slack_bot_token)
        self.slack_channel_name = slack_channel_name

    def post_sk8date(self, message_text):
        self.client.api_call(
            "chat.postMessage", channel=self.slack_channel_name, text=message_text
        )


class TelegramMessageProducer:

    TELEGRAM_URL = "https://api.telegram.org/bot"

    def __init__(self, bot_token=settings.TELEGRAM_BOT_TOKEN):
        self.bot_token = bot_token

    def _build_url(self, api_action):
        return "{}{}/{}".format(self.TELEGRAM_URL, self.bot_token, api_action)

    def send_message(self, message, chat_id):
        data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        requests.post(self._build_url("sendMessage"), data=data)

    def send_photo(self, chat_id, photo):
        data = {"chat_id": chat_id, "photo": photo}
        requests.post(self._build_url("sendPhoto"), data=data)
