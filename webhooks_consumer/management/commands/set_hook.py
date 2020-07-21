import json
import requests

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse


class Command(BaseCommand):
    help = "Sets webhook for local Telegram bot dev environment"

    def add_arguments(self, parser):
        parser.add_argument("--address", type=str, help="ngrok forwarding address")

    def handle(self, *args, **options):
        if options["address"]:
            ngrok_address = options["address"].strip().replace("https://", "")
        else:
            self.stdout.write("Please provide --address")

        telegram_url = "https://api.telegram.org/bot{}/setWebhook?url=https://{}{}".format(
            settings.TELEGRAM_BOT_TOKEN, ngrok_address, reverse("webhook-telegram")
        )
        response = requests.get(telegram_url)
        returned_data = json.loads(response.content)
        self.stdout.write(json.dumps(returned_data, indent=4, sort_keys=True))
        assert response.status_code == 200
