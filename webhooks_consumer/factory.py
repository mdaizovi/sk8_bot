import json
import random
import requests
from bs4 import BeautifulSoup
from slackclient import SlackClient

from django.conf import settings


class GenericMessageFactory:
    def __init__(self,request_json):
        self.request_json = request_json
        # APIS to look into lateR:
        # https://favqs.com/api
        # https://theysaidso.com/api/#
        # http://paperquotes.com/

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

    def _get_pet(self):
        pet_function = random.choice([self._get_kitty, self._get_doggo])
        url = pet_function()
        return url

    def _get_fox(self):
        api_url = "https://randomfox.ca/floof/"
        contents = requests.get(api_url).json()
        url = contents["image"]
        return url

    def _get_insult(self):
        api_url = "https://autoinsult.com/index.php?style={}".format(random.randint(0,3))
        contents = requests.get(api_url)
        soup = BeautifulSoup(contents.content, 'html.parser')
        text = soup.find("div", {"id": "insult"}).getText()
        return text

    def _get_taco(self):
        api_url = "http://taco-randomizer.herokuapp.com/random/"
        contents = requests.get(api_url).json()
        text = json.dumps(contents, indent=4, sort_keys=True)
        return text

    def _parse_telegram_message_obj(self):
        return self.request_json["message"]

    def _parse_telegram_chat_obj(self):
        return self._parse_telegram_message_obj()["chat"]

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
                "{} not in {}; wrong method called".format(command_str, msg_str)
            )

    def _get_broadcast_message(self):
        # message string may come from Telegram or Slack. Decide which it is and parse accodringly.
        if set(dict(self.request_json).keys()) == set(['update_id', 'message']):
            # Telegram json
            message_list = self._parse_telegram_message_string().split()
            message_text = " ".join(message_list[1:])
            sender = self._parse_telegram_sender_string()
            platform = "Telegram"
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
        url = "https://api.telegram.org/bot{}/{}".format(settings.TELEGRAM_BOT_TOKEN, api_action)
        return url

    def _send_output(self, output_target, output_content):
        has_image_extension = [True for ext in ["jpg", "jpeg", "png", "gif", "mp4", "webm"] if output_content.lower().endswith(".{}".format(ext))]
        if "http" in output_content and any(has_image_extension): # it's a photo 
            data = {"chat_id": output_target, "photo": output_content}
            requests.post(self._build_url(api_action="sendPhoto"), data=data)
        else:
            data = {"chat_id": output_target, "text": output_content, "parse_mode": "Markdown"}
            requests.post(self._build_url(api_action="sendMessage"), data=data)
            
            
class SlackMessageFactory(GenericMessageFactory):

    def __init__(self, request_json):
        super().__init__(request_json)

    def _send_output(self, output_target, output_content):
        slack_client = SlackClient(settings.SLACK_BOT_TOKEN)
        response = slack_client.api_call(
            "chat.postMessage", channel=output_target, text=output_content
        )

