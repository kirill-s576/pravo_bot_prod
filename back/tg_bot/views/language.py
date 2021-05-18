from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404
from django.conf import settings

from ..models import Language
from ..serializers import (
    BotLanguageListSerializer,
    BotLanguageCreateSerializer,
    BotLanguageUpdateSerializer
)

class BotLanguageViewSet(ViewSet):

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Languages list', BotLanguageListSerializer(many=True)),
        },
        tags=['Bot__Languages']
    )
    def list(self, request):
        """ Method returns all available languages """
        models = Language.objects.all()
        serializer = BotLanguageListSerializer(models, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=BotLanguageCreateSerializer,
        responses={
            200: openapi.Response('Created language', BotLanguageListSerializer),
        },
        tags=['Bot__Languages']
    )
    def create(self, request):
        serializer = BotLanguageCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_model = serializer.create(serializer.validated_data)
            new_serializer = BotLanguageListSerializer(new_model)
            return Response(new_serializer.data, status=200)
        else:
            return Response({"error": "Serializer isn't valid"}, status=400)

    @swagger_auto_schema(
        request_body=BotLanguageUpdateSerializer,
        responses={
            200: openapi.Response('Updated Language', BotLanguageListSerializer),
        },
        tags=['Bot__Languages']
    )
    def update(self, request, pk=None):
        serializer = BotLanguageUpdateSerializer(data=request.data)
        instance = get_object_or_404(Language, pk=pk)
        if serializer.is_valid():
            new_instance = serializer.update(instance=instance, validated_data=serializer.validated_data)
            new_serializer = BotLanguageListSerializer(new_instance)
            return Response(new_serializer.data, status=200)
        else:
            return Response({"error": "Serializer isn't valid"}, status=400)

    @swagger_auto_schema(
        tags=['Bot__Languages']
    )
    def destroy(self, request, pk=None):
        instance = get_object_or_404(Language, pk=pk)
        instance.delete()
        return Response(status=200)

    @swagger_auto_schema(
        tags=['Bot__Languages']
    )
    @action(methods=["GET"], detail=False)
    def get_choices(self, request):
        lang_choices = settings.LANG_CHOICES
        lang_choices = [
            {
                "label": lang[0],
                "name": lang[1]
            } for lang in lang_choices
        ]
        return Response(lang_choices, status=200)