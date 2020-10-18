import requests

from django.db import models
from django.conf import settings

from slackclient import SlackClient

from .model_choices import PlatformChoices

class TelegramChat(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    chat_id = models.CharField(max_length=100, db_index=True)
    bot = models.ForeignKey(
        "Bot", null=True, blank=True, on_delete=models.SET_NULL, related_name="telegram_chat"
    )
    
    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.name if self.name else self.chat_id)
        
        
class TelegramChannel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    channel_id = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.name if self.name else self.channel_id)        
        
        
    # ---------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        # IMPORTANT: channel IDs are always negative and 13 characters long.
        if self.channel_id[-1] != "-":
            self.channel_id = "-" + self.channel_id
        if len(self.channel_id) < 14:
            fragment = self.channel_id[1:]
            current_len = len(fragment)
            difference = 13 - len(fragment)
            new = "".join(["0" for s in range(difference)])
            self.channel_id = "-" + new + fragment
        super().save()
        
class Bot(models.Model):
    TELEGRAM_URL = "https://api.telegram.org/bot"
    BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
    SLACK_CLIENT = None
    
    name = models.CharField(max_length=100, null=True, blank=True)
    telegram_channel = models.ForeignKey(
        TelegramChannel, null=True, blank=True, on_delete=models.SET_NULL
    )

    # i think slack_team_id  is useless, don't remember why i added it
    slack_team_id = models.CharField(max_length=100, null=True, blank=True)
    slack_bot_token = models.CharField(max_length=100, null=True, blank=True)
    slack_channel_name = models.CharField(max_length=100, null=True, blank=True, help_text="The Slack Channel the Bot will post to")

    # ---------------------------------------------------------------------------
    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.name)

    def _build_url(self, api_action):
        return "{}{}/{}".format(self.TELEGRAM_URL, self.BOT_TOKEN, api_action)

    def _slack_client(self):
        self.SLACK_CLIENT = SlackClient(slack_bot_token)

    def _slack_post(self, message_text):
        if not self.SLACK_CLIENT:
            self._slack_client()
        self.SLACK_CLIENT.api_call(
            "chat.postMessage", channel=self.slack_channel_name, text=message_text
        )

    def _telegram_send_message(self, message, chat_id):
        data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        requests.post(self._build_url("sendMessage"), data=data)

    def _telegram_send_photo(self, chat_id, photo):
        data = {"chat_id": chat_id, "photo": photo}
        requests.post(self._build_url("sendPhoto"), data=data)


# I'm not using this yet, maybe get rid of it.
class BotAction(models.Model):
    command = models.CharField(max_length=100, help_text = "the command that triggers function, like /sk8")
    function = models.CharField(max_length=100, help_text = "function name that is triggered")
    bot = models.ForeignKey(
        "Bot", on_delete=models.CASCADE
    )
    