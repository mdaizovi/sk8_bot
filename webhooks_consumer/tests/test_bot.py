import json
import pytest
import requests
from time import sleep
from pyrogram import Client

from django.conf import settings
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse

from webhooks_consumer.models import Bot


class MyServerTests(LiveServerTestCase):
    port = 8000  # if address already in use, run pkill -9 -f 8000
    telegram_client = None
    chat_id = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        if Bot.objects.count() < 1:  # don't do if re-using db
            telegram_chat_id = input(
                "\n\nWhat is your test telegram_chat_id?\n"
            ).strip()
            MyServerTests.chat_id = telegram_chat_id
            telegram_channel_id = input(
                "\nWhat is your test telegram_channel_id?\n"
            ).strip()
            slack_team_id = input("\nWhat is your test slack_team_id?\n").strip()
            slack_bot_token = input("\nWhat is your test slack_bot_token?\n").strip()
            bot_dict = {
                "telegram_chat_id": telegram_chat_id,
                "telegram_channel_id": telegram_channel_id,
                "slack_team_id": slack_team_id,
                "slack_bot_token": slack_bot_token,
                "slack_channel_name": "bot-test",
            }
            print(bot_dict)
            bot = Bot.objects.get_or_create(**bot_dict)
            print(bot)

        ngrok_address = (
            input(
                "\n-----Please start a new ngrok session in another terminal (old session might fail silently)"
                " by typing './ngrok http 8000'\n\nNow tell me what is the Forwarding URL?\n"
            )
            .strip()
            .replace("https://", "")
        )
        telegram_url = "https://api.telegram.org/bot{}/setWebhook?url=https://{}{}".format(
            settings.TELEGRAM_BOT_TOKEN, ngrok_address, reverse("webhook-telegram")
        )
        response = requests.get(telegram_url)
        returned_data = json.loads(response.content)
        print(returned_data)
        assert response.status_code == 200
        print("\nAbout to instantiate Client")
        MyServerTests.telegram_client = Client(
            "my_session",
            settings.TELEGRAM_APP_API_ID,
            settings.TELEGRAM_APP_API_HASH,
            test_mode=True,
        )
        print("About to start client")
        MyServerTests.telegram_client.start()
        print("Client started")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("About to stop client")
        MyServerTests.telegram_client.stop()
        print("Client stopped")

    @pytest.mark.django_db
    def test_logged_in_to_test_account(self):
        me_obj = MyServerTests.telegram_client.get_me()
        assert me_obj["first_name"] == "Mic Test"
        assert me_obj["username"] == "MicTest"

    @pytest.mark.django_db
    def test_a_normal_chatter(self):
        sleep(5)
        MyServerTests.telegram_client.send_message(
            MyServerTests.chat_id, "Starting test suite"
        )
        sleep(5)

    @pytest.mark.django_db
    def test_b_doggo(self):
        MyServerTests.telegram_client.send_message(MyServerTests.chat_id, "/doggo")
        #  Give time for the dog to show up
        sleep(10)
        # later assert last message in chat is a pic of a dog. don't feel like automating it now, just look at your phone.

    @pytest.mark.django_db
    def test_c_sk8(self):
        MyServerTests.telegram_client.send_message(
            MyServerTests.chat_id, "/sk8 always hooray!"
        )
        #  Give time for the message to show up
        sleep(10)
        # later assert last message in chat is a compliment, and channel has an update.
        # don't feel like automating it now, just look at your phone.

    def test_d_end(self):
        MyServerTests.telegram_client.send_message(
            MyServerTests.chat_id, "Ending test suite"
        )
        sleep(5)
