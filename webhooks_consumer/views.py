import json
import urllib

from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse

from .consumer import TelegramMessageConsumer, SlackMessageConsumer

from .models import Bot, TelegramChat


class TelegramBotView(View):
    # https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhooks/tutorial/
    # https://core.telegram.org/bots/webhooks

    def get(self, request, *args, **kwargs):
        """
        Just to test deployment is okay
        """
        return HttpResponse("Hi!")

    def post(self, request, *args, **kwargs):
        request_json = json.loads(request.body.decode("utf-8"))
        #print(json.dumps(request_json, indent=4, sort_keys=True))
        if "message" not in request_json:
            return JsonResponse({"ok": "no message to process"})

        try:
            t_message = request_json["message"]
            chat_id = request_json["message"]["chat"]["id"]
            text = t_message["text"].strip().lower()
            try:
                chat = TelegramChat.objects.get(chat_id=chat_id)
                bot = chat.bot
            except:
                return JsonResponse({"ok": "Bot not found; command ignored"})

        except Exception as e:
            return JsonResponse({"ok": "No message text to process"})

        if text[0] == "/":  # If it's not a command we do nothing
            textlist = text.split()
            command = textlist[0]
            telegram_consumer = TelegramMessageConsumer(
                request_json=request_json, bot=bot
            )

            if command in telegram_consumer.bound_method_dict.keys():
                method = getattr(
                    telegram_consumer, telegram_consumer.bound_method_dict.get(command)
                )
                method()
                return JsonResponse({"ok": "POST request processed"})
            else:
                msg = "WTF?!?"
                bot._telegram_send_message(
                    message=msg, chat_id=telegram_consumer._get_chat_obj()["id"]
                )

        return JsonResponse({"ok": "no need to process"})


class SlackBotView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hi!")

    def post(self, request, *args, **kwargs):
        response_dict = {"blocks": [{"type": "section", "text": {"type": "mrkdwn",},}]}
        request_dict = {
            k.decode("utf-8"): v.decode("utf-8")
            for k, v in urllib.parse.parse_qsl(request.body)
        }

        slack_team_id = request_dict["team_id"]
        try:
            bot = Bot.objecs.get(slack_team_id=slack_team_id)
        except:
            bot = None
            response_text = "Bot with slack team id not found; command ignored"

        if bot:
            command = request_dict["command"]
            slack_consumer = SlackMessageConsumer(request_dict)
            method = getattr(
                slack_consumer, slack_consumer.bound_method_dict.get(command)
            )
            response_obj = method()
            response_text = "Thanks!"

        response_dict["blocks"][0]["text"]["text"] = response_text
        return JsonResponse(response_dict)
