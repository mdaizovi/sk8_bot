from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import TelegramBotView, SlackBotView

urlpatterns = [
    path(
        "telegrambot/", csrf_exempt(TelegramBotView.as_view()), name="webhook-telegram"
    ),
    path("slackbot/", csrf_exempt(SlackBotView.as_view()), name="webhook-slack"),
]
