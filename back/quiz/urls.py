from rest_framework.routers import SimpleRouter
from .views import QButtonViewSet
from .views import MessageViewSet
from .views import StageViewSet
from .views import LanguageViewSet
from .views import MessageTranslationViewSet, QButtonTranslationViewSet


router = SimpleRouter()

router.register("buttons", QButtonViewSet, basename="Buttons")
router.register("messages", MessageViewSet, basename="Texts")
router.register("stages", StageViewSet, basename="Stages")
router.register("languages", LanguageViewSet, basename="Languages")
router.register("translates/message", MessageTranslationViewSet, basename="MessageTranslation")
router.register("translates/button", QButtonTranslationViewSet, basename="ButtonTranslation")

urlpatterns = router.urls
