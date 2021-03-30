from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import telebot


class BotViewSet(ViewSet):

    @action(methods=["GET"], detail=False)
    def set_web_hook(self, request):
        return Response()

    @action(methods=["GET"], detail=False)
    def remove_web_hook(self, request):
        return Response()

    @action(methods=["POST"], detail=False)
    def process_request(self, request):
        bot = telebot.TeleBot()
        bot.process_new_updates([telebot.types.Update.de_json(request.data)])
        print(request.data)
