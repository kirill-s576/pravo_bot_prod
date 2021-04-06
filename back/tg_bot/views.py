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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


BOT_TOKEN = settings.BOT_TOKEN
SERVER_HOST = settings.SERVER_HOST


class BotViewSet(ViewSet):

    @swagger_auto_schema(
        tags=['Bot']
    )
    @action(methods=["GET"], detail=False)
    def users(self, request):
        return Response({}, status=200)


@csrf_exempt
def bot_webhook(request, token):
    """ Handler for Webhook from telegram """
    logic_module_kwarg = {
        "language_model": Language,
        "message_model": Message,
        "user_model": BotUser,
        "quiz_interface": SessionInterface
    }
    if token == BOT_TOKEN:
        try:
            bot = Bot(BOT_TOKEN, DjangoRegisterBotLogicModule, logic_module_kwarg)
            bot.process_updates([telebot.types.Update.de_json(request.body.decode("utf-8"))])
            return JsonResponse({"success": True}, status=200)
        except Exception as e:
            return JsonResponse({"success": False}, status=500)
    else:
        return JsonResponse({"error": "Token not found"}, status=404)