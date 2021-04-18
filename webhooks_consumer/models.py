import requests

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from .model_choices import PlatformChoices, FunctionChoices

class InputSource(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    nickname_public = models.CharField(max_length=10, null=True, blank=True, help_text="nickname for bulletins. ex: 'nic on BSC', with BSC insread of Telegram")
    chat_id = models.CharField(max_length=100, db_index=True, help_text="Might be Telegram group chat_id, might be Slack team_id")
    platform = models.CharField(
        help_text="Telegram, Slack, etc",
        choices=PlatformChoices.CHOICES, max_length=10, default=PlatformChoices.TELEGRAM
    )
    actions = models.ManyToManyField("BotAction", blank=True)
    
    def __str__(self):
        return "{}: {} ({})".format(self.__class__.__name__, self.name if self.name else self.chat_id, self.get_platform_display())
            
class OutputChannel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    channel_id = models.CharField(max_length=100, db_index=True)
    platform = models.CharField(
        help_text="Telegram, Slack, etc",
        choices=PlatformChoices.CHOICES, max_length=10, default=PlatformChoices.TELEGRAM
    )
    
    def __str__(self):
        return "{}: {} ({})".format(self.__class__.__name__, self.name if self.name else self.channel_id, self.get_platform_display())        
        
    # ---------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        # IMPORTANT: Tenegram channel IDs are always negative and 13 characters long.
        if self.platform == PlatformChoices.TELEGRAM:
            if self.channel_id[0] != "-":
                self.channel_id = "-" + self.channel_id
            if len(self.channel_id) < 14:
                fragment = self.channel_id[1:]
                current_len = len(fragment)
                difference = 13 - len(fragment)
                new = "".join(["0" for s in range(difference)])
                self.channel_id = "-" + new + fragment
        super().save()


class BotOutput(models.Model):
    output_function = models.CharField(
        help_text="Function that gets text or image that will be sent somewhere",
        choices=FunctionChoices.CHOICES, max_length=20
    )
    output_platform = models.CharField(
        help_text="Telegram, Slack, etc",
        choices=PlatformChoices.CHOICES, max_length=10
    )
    output_channel = models.ForeignKey(
        OutputChannel, help_text="Where the output goes. If None, will go to source", null=True, blank=True, on_delete=models.CASCADE
    )
    
    def __str__(self):
        return "{}: {} on {}".format(self.__class__.__name__, self.output_function, self.output_channel)      

    # def clean(self):
    #     pass
    # 
    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     return super().save(*args, **kwargs)

    def get_factory(self):
        return PlatformChoices.get_factory(self.output_platform)

    def get_factory_method_content(self, factory):
        method = getattr(factory, "_get_{}".format(self.output_function))
        # content will be either a string of what to post, or an image.
        content = method()
        return content    

class BotAction(models.Model):
    command = models.CharField(max_length=100, help_text = "the command that triggers function, like /sk8")
    content_required = models.BooleanField(default=False, help_text = "Does the message require content? EG sk8 True, doggo False")
    output = models.ManyToManyField("BotOutput")
    
    @property
    def output_display(self):
        return ",".join([str(o.output_channel) for o in self.output.all()])   
    
    def __str__(self):
        return "{}: {} {}".format(self.__class__.__name__, self.command, self.output_display)      

