import json
import urllib

from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponse

from .factory import SlackMessageFactory, TelegramMessageFactory

from .models import InputSource, OutputChannel, BotAction, BotOutput
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
                chat = InputSource.objects.get(chat_id=chat_id, input_platform=PlatformChoices.TELEGRAM)
            except:
                return JsonResponse({"ok": "Input source not found; command ignored"})

        except Exception as e:
            return JsonResponse({"ok": "No message text to process"})

        
        if text[0] == "/":  # If it's not a command we do nothing
            textlist = text.split()
            command = textlist[0].replace("/", "")
            try:
                botaction = chat.botaction_set.get(command=command, input_platform=PlatformChoices.TELEGRAM)
                
            except BotAction.DoesNotExist:
                factory = TelegramMessageFactory(request_json)
                factory._send_output(output_target=chat_id, output_content="WTF?!?")
                return JsonResponse({"ok": "Action not found"})
            
            for o in botaction.output.all():
                factory_class = o.get_factory()
                factory = factory_class(request_json=request_json)
                content = o.get_factory_method_content(factory =factory)
                
                output_channel = o.output_channel.channel_id
                if not output_channel:
                    output_channel = chat_id 
                factory._send_output(output_target=output_channel, output_content=content)
                
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
        if settings.ENV_TYPE == "develop":
            print(json.dumps(request_json, indent=4, sort_keys=True))
        else:
            print(request_json)


        slack_team_id = request_dict["team_id"]
        try:
            inputsource = InputSource.objects.get(chat_id=slack_team_id, input_platform=PlatformChoices.SLACK)
        except:
            response_text = "Input with slack team id not found; command ignored"

        if not response_text:
            command = request_dict["command"]
            try:
                botaction = inputsource.botaction_set.get(command=command, input_platform=PlatformChoices.SLACK)
            except BotAction.DoesNotExist:
                 response_text = "Source has no action for {}".format(command)
            
            if not response_text:
                for o in botaction.output.all():
                    factory_class = o.get_factory()
                    factory = factory_class(request_json=request_json)
                    content = o.get_factory_method_content(factory =factory)
                    output_channel = o.output_channel.channel_id
                    factory._send_output(output_target=output_channel, output_content=content)
                response_text = "Thanks!"
                
        response_dict["blocks"][0]["text"]["text"] = response_text
        return JsonResponse(response_dict)
