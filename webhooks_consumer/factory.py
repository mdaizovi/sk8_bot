import json
import random
import requests
from slackclient import SlackClient

from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMessage, send_mail, mail_admins

class GenericMessageFactory:
    def __init__(self, request_json):
        self.request_json = request_json
        # APIS to look into lateR:
        # https://favqs.com/api
        # https://theysaidso.com/api/#
        # http://paperquotes.com/

    def _get_api_response_or_none(self, api_url):
        try:
            response = requests.get(api_url, timeout=10)
            contents = response.json()
            return contents
        except:
            return

    def _get_compliment(self):
        api_url = "https://complimentr.com/api"
        contents = self._get_api_response_or_none(api_url)
        if contents:
            compliment = contents["compliment"]
            return compliment
        return None

    def _get_doggo(self):
        # oh no! doggo is down!
        # api_url = "https://random.dog/woof.json"
        # contents = self._get_api_response_or_none(api_url)
        # if contents and "url" in contents:
        #     url = contents["url"]
        #     return url
        # return None

        # Not as cute dog api
        api_url = "https://dog.ceo/api/breeds/image/random"
        contents = self._get_api_response_or_none(api_url)
        if contents and "message" in contents:
            url = contents["message"]
            return url

    def _get_duck(self):
        api_url = "https://random-d.uk/api/v2/random"
        contents = self._get_api_response_or_none(api_url)
        if contents:
            url = contents["url"]
            return url
        return None

    def _get_sloth(self):
        # doesn't work aymore
        api_url = "https://sloth.pics/api"
        contents = self._get_api_response_or_none(api_url)
        if contents:
            url = contents["url"]
            return url
        return None

    def _get_bootie(self):
        sayings = [
            "Jesus titty fucking Christ!",
            "Fuck me dead and bury me pregnant!",
            "Fuck MY DAD and bury me pregnant",
            "I'm not here to fuck spiders",
            "G'day mate!",
            "Bend your knees!",
            "Look behind you!",
            "A millimeter higher, a millisecond faster",
            "It’s better to be looked over than overlooked",
            "Noiiice!!!",
            "aaaawww SHIT Yeah!",
            "Fucking hell dude!"
        ]
        return random.choice(sayings)

    def _get_kitty(self):
        api_url = "https://api.thecatapi.com/v1/images/search"
        contents = self._get_api_response_or_none(api_url)
        if contents:
            url = contents[0]["url"]
            return url
        return None

    def _get_pet(self):
        pet_function = random.choice([self._get_kitty, self._get_doggo])
        url = pet_function()
        return url

    def _get_fox(self):
        api_url = "https://randomfox.ca/floof/"
        contents = self._get_api_response_or_none(api_url)
        if contents:
            url = contents["image"]
            return url
        return None

    def _get_taco(self):
        # doesn't work aymore
        api_url = "http://taco-randomizer.herokuapp.com/random/"
        contents = self._get_api_response_or_none(api_url)
        if contents:
            text = json.dumps(contents, indent=4, sort_keys=True)
            return text
        return None

    def _parse_telegram_message_obj(self):
        return self.request_json["message"]

    def _parse_telegram_chat_obj(self):
        return self._parse_telegram_message_obj()["chat"]

    def _parse_telegram_chat_id(self):
        t_chat = self._parse_telegram_chat_obj()
        return t_chat.get("id")

    def _parse_telegram_sender_string(self):
        t_chat = self._parse_telegram_chat_obj()
        if "sender" in t_chat:
            obj = t_chat
        else:
            obj = self._parse_telegram_message_obj()["from"]
        return obj.get("first_name")

    def _parse_telegram_message_string(self):
        return self._parse_telegram_message_obj()["text"]

    def _parse_slack_command_message_string(self):
        return self.request_json["text"]

    def _parse_slack_sender_string(self):
        return self.request_json["user_name"]

    def _parse_telegram_command_message_string(self, command_str):
        msg_str = self._parse_telegram_message_string().strip().lower()
        if command_str in msg_str:
            message_list = msg_str.split("/{} ".format(command_str))
            if len(message_list) > 1:
                command_content = message_list[1]
                return command_content
        else:
            raise ValueError(
                "{} not in {}; wrong method called".format(
                    command_str, msg_str)
            )

    def _get_broadcast_message(self):
        # message string may come from Telegram or Slack. Decide which it is and parse accordingly.
        if set(dict(self.request_json).keys()) == set(['update_id', 'message']):
            # Telegram json
            message_list = self._parse_telegram_message_string().split()
            message_text = " ".join(message_list[1:])
            sender = self._parse_telegram_sender_string()
            platform = "Telegram"
            try:
                chat_id = self._parse_telegram_chat_id()
                if chat_id:
                    # Getting around circular import issue, bc I import from .factory in .model_choices and then import .model_choices in .models
                    InputSource = apps.get_model(
                        "webhooks_consumer.InputSource")
                    telegram_input = InputSource.objects.get(chat_id=chat_id)
                    if telegram_input:
                        if telegram_input.nickname_public:
                            platform = telegram_input.nickname_public
                        else:
                            platform = telegram_input.get_platform_display()  # Should be Telegram
            except:
                message_body = "A bot post failed in get_broadcast_message. go look at it."
                mail_admins(subject="Failed Bot post", message = message_body, fail_silently=True)
        else:
            # Slack json
            platform = "Slack"
            message_text = self._parse_slack_command_message_string()
            sender = self._parse_slack_sender_string()

        broadcast_msg = "{} on {}: {}".format(
            sender if sender else "", platform, message_text
        )
        return broadcast_msg

    def _send_output(self):
        raise NotImplementedError(
            "_send_output has not been implemented for {}".format(
                self.__class__.__name__
            )
        )


class TelegramMessageFactory(GenericMessageFactory):

    def __init__(self, request_json):
        super().__init__(request_json)

    def _build_url(self, api_action):
        url = "https://api.telegram.org/bot{}/{}".format(
            settings.TELEGRAM_BOT_TOKEN, api_action)
        return url

    def _send_output(self, output_target, output_content):
        has_image_extension = [True for ext in ["jpg", "jpeg", "png", "gif",
                                                "mp4", "webm"] if output_content.lower().endswith(".{}".format(ext))]
        # it's a photo
        if "http" in output_content and any(has_image_extension):
            data = {"chat_id": output_target, "photo": output_content}
            requests.post(self._build_url(api_action="sendPhoto"), data=data)
        else:
            data = {"chat_id": output_target,
                    "text": output_content, "parse_mode": "Markdown"}
            
            response = requests.post(self._build_url(api_action="sendMessage"), data=data)
            print(response.content)
#             message_body = "A bot post failed. go look at it."
#             mail_admins(subject="Failed Bot post", message = message_body, fail_silently=True)



class SlackMessageFactory(GenericMessageFactory):

    def __init__(self, request_json):
        super().__init__(request_json)

    def _send_output(self, output_target, output_content):
        slack_client = SlackClient(settings.SLACK_BOT_TOKEN)
        response = slack_client.api_call(
            "chat.postMessage", channel=output_target, text=output_content
        )
