from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import telebot
from django.conf import settings
from tg_bot.models import BotUser, Message, Language
from quiz.interface import SimpleInterface, SessionInterface
from tg_bot.logic_module import LogicModule, DjangoRegisterBotLogicModule
from .interface import Bot

BOT_TOKEN = settings.BOT_TOKEN
SERVER_HOST = settings.SERVER_HOST


class BotViewSet(ViewSet):

    @swagger_auto_schema(
        tags=['Bot']
    )
    @action(methods=["GET"], detail=False)
    def set_web_hook(self, request):
        return Response({})

    @swagger_auto_schema(
        tags=['Bot']
    )
    @action(methods=["GET"], detail=False)
    def remove_web_hook(self, request):
        return Response({})

    @swagger_auto_schema(
        tags=['Bot']
    )
    def update(self, request, pk=None):
        logic_module_kwarg = {
            "language_model": Language,
            "message_model": Message,
            "user_model": BotUser,
            "quiz_interface": SessionInterface
        }
        if pk != BOT_TOKEN:
            return Response({"error": "Token not found"}, status=404)
        bot = Bot(BOT_TOKEN, DjangoRegisterBotLogicModule, logic_module_kwarg)
        bot.process_updates([telebot.types.Update.de_json(request.data)])
        return Response({}, status=200)
