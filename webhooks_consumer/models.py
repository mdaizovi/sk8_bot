import requests

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from .factory import SlackMessageFactory, TelegramMessageFactory

from .model_choices import *

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


class BotOutput(models.Model):
    output_function = models.CharField(
        help_text="Function that gets text or image that will be sent somewhere",
        choices=FunctionChoices.CHOICES, max_length=20
    )
    output_platform = models.CharField(
        help_text="Telegram, Slack, etc",
        choices=PlatformChoices.CHOICES, max_length=10
    )
    output_telegram_channel = models.ForeignKey(
        TelegramChannel, help_text="Where the output goes. If None, will go to source", null=True, blank=True, on_delete=models.CASCADE
    )
    output_slack_channel = models.CharField(max_length=100, null=True, blank=True, help_text="The Slack Channel the Bot will post to")

    def __str__(self):
        return "{}: {} on {}".format(self.__class__.__name__, self.output_function, self.output_telegram_channel if self.output_telegram_channel else self.output_slack_channel)      

    def clean(self):
        channel_attr_list =["output_telegram_channel", "output_slack_channel"]
        get_channel_list = [True for x in channel_attr_list if getattr(self, x)]
        if len(get_channel_list) > 1 :
            raise ValidationError("Please choose only 1 of {}".format(", ".join(channel_attr_list)))
            
        # platform_channel_dict = {PlatformChoices.TELEGRAM: "output_telegram_channel", PlatformChoices.SLACK:"output_slack_channel"}
        # output_field_name = platform_channel_dict.get(self.output_platform)
        # if not getattr(self, output_field_name) and 
        #     raise ValidationError("You need to provide {} if you want to output on {}".format(output_field_name, self.output_platform))
        if self.output_platform == PlatformChoices.SLACK and not self.output_slack_channel:
            raise ValidationError("You need to provide {} if you want to output on {}".format(self.output_slack_channel, self.output_platform))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_factory(self):
        factories = {PlatformChoices.TELEGRAM: TelegramMessageFactory, PlatformChoices.SLACK: SlackMessageFactory}
        return factories.get(self.output_platform)

    def get_output_channel(self):
        channel_attr_list = ["output_telegram_channel", "output_slack_channel"]
        for c in channel_attr_list:
            val = getattr(self, c)
            if val:
                # since this is a nested object but slack is jsut text. should make more consistent.
                if hasattr(val, "channel_id"):
                    return getattr(val, "channel_id")
                else:
                    return val
                
        

class BotAction(models.Model):
    command = models.CharField(max_length=100, help_text = "the command that triggers function, like /sk8")
    bot = models.ForeignKey(
        "Bot", help_text = "The Bot that listens to this command and execites this action", on_delete=models.CASCADE
    )
    output = models.ManyToManyField("BotOutput")
    
    def __str__(self):
        return "{}: {} on {}".format(self.__class__.__name__, self.command, self.bot)      

    