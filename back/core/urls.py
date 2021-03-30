from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Bot Api",
        default_version='v1',
        description="It is API for changes and controls of Bot"
    ),
    public=True,
    url='https://telbot.refugee.ru/',
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^doc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # JWT Auth
    path('auth/token', TokenObtainPairView.as_view(), name='create_token'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='refresh_token'),

    path('quiz/', include("quiz.urls")),
    path('auth/', include("user.urls")),
]
