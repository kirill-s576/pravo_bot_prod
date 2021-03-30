from rest_framework.routers import SimpleRouter
from .views import BotViewSet, bot_webhook
from django.urls import path

urlpatterns = [
    path('bot/<token>/', bot_webhook, name="bot_webhook")
]

router = SimpleRouter()
router.register("", BotViewSet, basename="Bot")
urlpatterns += router.urls

