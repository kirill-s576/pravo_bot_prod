from rest_framework.routers import SimpleRouter
from .views import CustomUserViewSet

router = SimpleRouter()

router.register("user", CustomUserViewSet, basename="User")

urlpatterns = router.urls
