from rest_framework.routers import SimpleRouter
from .views import BotViewSet


router = SimpleRouter()

router.register("", BotViewSet, basename="Bot")

urlpatterns = router.urls
