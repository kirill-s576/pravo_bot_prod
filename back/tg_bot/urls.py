from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import (BotViewSet,
                    BotLanguageViewSet,
                    BotMessageViewSet,
                    BotTranslateViewSet,
                    bot_webhook)


urlpatterns = [
    path('bot/<token>/', bot_webhook, name="bot_webhook")
]

router = SimpleRouter()
router.register("", BotViewSet, basename="Bot")
router.register("languages", BotLanguageViewSet, basename="Language")
router.register("messages", BotMessageViewSet, basename="Message")
router.register("translates", BotTranslateViewSet, basename="Translate")
urlpatterns += router.urls

