import random
import requests

from django.conf import settings


class MessageConsumer:
    def __init__(self, bot, request_json):
        self.bot = bot
        self.request_json = request_json
        self.bound_method_dict = {"/sk8": "sk8"}

    def _get_compliment(self):
        api_url = "https://complimentr.com/api"
        contents = requests.get(api_url).json()
        compliment = contents["compliment"]
        return compliment

    def _get_doggo(self):
        api_url = "https://random.dog/woof.json"
        contents = requests.get(api_url).json()
        url = contents["url"]
        return url

    def _get_kitty(self):
        api_url = "https://api.thecatapi.com/v1/images/search"
        contents = requests.get(api_url).json()
        url = contents[0]["url"]
        return url

    def _build_broadcast_message(self, sender, message_text):
        broadcast_msg = "{} on {}: {}".format(
            sender if sender else "", self._get_platform(), message_text
        )
        return broadcast_msg

    def _get_platform(self, name):
        raise NotImplementedError(
            "_get_platform has not been implemented for {}".format(
                self.__class__.__name__
            )
        )


class SlackMessageConsumer(MessageConsumer):
    def __init__(self, bot, request_json, *args, **kwargs):
        super().__init__(bot, request_json, *args, **kwargs)

    def _get_platform(self):
        return "Slack"

    def _get_command_message_string(self):
        return self.request_json["text"]

    def _get_sender_string(self):
        return self.request_json["user_name"]

    def sk8(self):
        text = self._get_command_message_string()
        if text and len(text) > 1:

            sender = self._get_sender_string()
            broadcast_msg = self._build_broadcast_message(sender, text)

            if settings.ENV_TYPE == "prod":
                self.bot._telegram_send_message(
                    message=broadcast_msg, chat_id=self.bot.telegram_channel_id
                )
                # if self.bot.slack_bot_token:
                #     slack_producer = SlackMessageProducer(
                #         slack_bot_token=self.bot.slack_bot_token
                #     )
                #     slack_producer.post_sk8date(broadcast_msg)

            # response_text = self._get_compliment()  # pythonanywhere doesn't support threading and this takes too long so slack times out
            response_text = "Thanks!"
        else:
            response_text = "Please include info about your skate date"

        return {"response_text": response_text}


class TelegramMessageConsumer(MessageConsumer):
    def _get_platform(self):
        return "Telegram"

    def __init__(self, bot, request_json, *args, **kwargs):
        super().__init__(bot, request_json, *args, **kwargs)
        self.bound_method_dict.update({"/doggo": "doggo", "/kitty":"kitty"})

    def _get_message_obj(self):
        return self.request_json["message"]

    def _get_chat_obj(self):
        return self._get_message_obj()["chat"]

    def _get_sender_string(self):
        t_chat = self._get_chat_obj()
        if "sender" in t_chat:
            obj = t_chat
        else:
            obj = self._get_message_obj()["from"]
        return obj.get("first_name")

    def _get_message_string(self):
        return self._get_message_obj()["text"]

    def _get_command_message_string(self, command_str):
        msg_str = self._get_message_string().strip().lower()
        if command_str in msg_str:
            message_list = msg_str.split("/{} ".format(command_str))
            if len(message_list) > 1:
                command_content = message_list[1]
                return command_content
        else:
            raise ValueError(
                "{} not in {}; wrong method called".format(command_str, msg_str)
            )

    def sk8(self):
        text = self._get_command_message_string("sk8")
        if text:
            if len(text) > 1:
                sender = self._get_sender_string()

                broadcast_msg = self._build_broadcast_message(sender, text)
                
                self.bot._telegram_send_message(
                    message=broadcast_msg, chat_id=self.bot.telegram_channel.channel_id
                )

                url_function = random.choice([self._get_kitty, self._get_doggo])
                url = url_function()
                self.bot._telegram_send_photo(chat_id=self._get_chat_obj()["id"], photo=url)

                # if all(
                #     [
                #         settings.ENV_TYPE == "prod",
                #         self.bot.slack_bot_token,
                #         self.bot.slack_channel_name,
                #     ]
                # ):
                #     slack_producer = SlackMessageProducer(
                #         slack_bot_token=self.bot.slack_bot_token,
                #         slack_channel_name=self.bot.slack_channel_name,
                #     )
                #     slack_producer.post_sk8date(broadcast_msg)

    def doggo(self):
        # Just to ensure correct method is being called
        self._get_command_message_string("doggo")
        url = self._get_doggo()
        self.bot._telegram_send_photo(chat_id=self._get_chat_obj()["id"], photo=url)
           
    def kitty(self):
        # Just to ensure correct method is being called
        self._get_command_message_string("kitty")
        url = self._get_kitty()
        self.bot._telegram_send_photo(chat_id=self._get_chat_obj()["id"], photo=url)