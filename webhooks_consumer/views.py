import json
import urllib

from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse

from .factory import SlackMessageFactory, TelegramMessageFactory

from .models import Bot, TelegramChat, BotAction
from .model_choices import FunctionChoices

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
        if settings.ENV_TYPE == "develop":
            print(json.dumps(request_json, indent=4, sort_keys=True))
        else:
            print(request_json)
            
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
            command = textlist[0].replace("/", "")
            try:
                botaction = bot.botaction_set.get(command=command)
                
            except BotAction.DoesNotExist:
                factory = TelegramMessageFactory(bot, request_json)
                factory._send_output(output_target=chat_id, output_content="WTF?!?")
                return JsonResponse({"ok": "Action not found"})
            
            for o in botaction.output.all():
                o.do_factory_method()
            return JsonResponse({"ok": "Action Completed"})

        return JsonResponse({"ok": "no need to process"})


class SlackBotView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hi!")

    def post(self, request, *args, **kwargs):
        response_text = None
        response_dict = {"blocks": [{"type": "section", "text": {"type": "mrkdwn",},}]}
        request_dict = {
            k.decode("utf-8"): v.decode("utf-8")
            for k, v in urllib.parse.parse_qsl(request.body)
        }
        request_json = json.loads(request_dict)

        slack_team_id = request_dict["team_id"]
        try:
            bot = Bot.objecs.get(slack_team_id=slack_team_id)
        except:
            bot = None
            response_text = "Bot with slack team id not found; command ignored"

        if bot:
            command = request_dict["command"]
            try:
                botaction = bot.botaction_set.get(command=command)
            except BotAction.DoesNotExist:
                 response_text = "Bot has no action for {}".format(command)
            
            if not response_text:
                for o in botaction.output.all():
                    o.do_factory_method()
                response_text = "Thanks!"
                
        response_dict["blocks"][0]["text"]["text"] = response_text
        return JsonResponse(response_dict)
