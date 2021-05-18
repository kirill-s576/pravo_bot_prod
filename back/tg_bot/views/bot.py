from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from tg_bot.models import BotUser, Message, Language
from tg_bot.logic_module import DjangoRegisterBotLogicModule

from quiz.interface import SimpleInterface, SessionInterface
from ..interface import Bot
from ..serializers.bot import SetWebhookSerializer
import telebot


BOT_TOKEN = settings.BOT_TOKEN
SERVER_HOST = settings.SERVER_HOST
BOT_LOGIC_MODULE_KWARGS = {
    "language_model": Language,
    "message_model": Message,
    "user_model": BotUser,
    "quiz_interface": SessionInterface
}


class BotViewSet(ViewSet):
    """
    Basic bot controls.
    """

    # Initialized interface for bor control
    bot_interface = Bot(BOT_TOKEN, DjangoRegisterBotLogicModule, BOT_LOGIC_MODULE_KWARGS)

    @swagger_auto_schema(
        request_body=SetWebhookSerializer,
        tags=['Bot']
    )
    @action(methods=["POST"], detail=False)
    def set_web_hook(self, request):
        """
        Set new url for bot webhook.
        """
        serializer = SetWebhookSerializer(data=request.data)
        if serializer.is_valid():
            response = self.bot_interface.set_web_hook(url=serializer.validated_data["url"])
            return Response({"telegram_response": response})
        return Response({"error": "Serializer isn't valid"}, status=400)

    @swagger_auto_schema(
        tags=['Bot']
    )
    @action(methods=["GET"], detail=False)
    def remove_web_hook(self, request):
        response = self.bot_interface.remove_web_hook()
        return Response({"telegram_response": response})

    @swagger_auto_schema(
        tags=['Bot']
    )
    @action(methods=["GET"], detail=False)
    def get_bot_info(self, request):
        response = self.bot_interface.get_web_hook_info()
        return Response({"telegram_response": response})


@csrf_exempt
def bot_webhook(request, token: str):
    """
    Handler for Webhook from telegram
    :token - Telegram Bot Token. You can get it from Bot Father.
    """

    if token == BOT_TOKEN:
        try:
            bot = Bot(BOT_TOKEN, DjangoRegisterBotLogicModule, BOT_LOGIC_MODULE_KWARGS)
            bot.process_updates([telebot.types.Update.de_json(request.body.decode("utf-8"))])
            return JsonResponse({"success": True}, status=200)
        except Exception as e:
            return JsonResponse({"success": False}, status=500)
    else:
        return JsonResponse({"error": "Token not found"}, status=404)