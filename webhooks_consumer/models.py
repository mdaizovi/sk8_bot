from django.db import models


class Bot(models.Model):
    telegram_chat_id = models.CharField(max_length=100, db_index=True)
    telegram_channel_id = models.CharField(max_length=100)

    slack_team_id = models.CharField(max_length=100, null=True, blank=True)
    slack_bot_token = models.CharField(max_length=100, null=True, blank=True)
    slack_channel_name = models.CharField(max_length=100, null=True, blank=True, help_text="The Slack Channel the Bot will post to")

    # ---------------------------------------------------------------------------
    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.telegram_chat_id,)

    # ---------------------------------------------------------------------------
    def save(self, *args, **kwargs):
        # IMPORTANT: channel IDs are always negative and 13 characters long.
        # TODO: write clean that adds 0s and makes negative if need be.
        super().save()
