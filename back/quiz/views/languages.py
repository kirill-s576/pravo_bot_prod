from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from django.conf import settings

from ..models import Language
from ..serializers import (
    LanguageReadSerializer,
    LanguageCreateSerializer,
    LanguageUpdateSerializer
)


class LanguageViewSet(ViewSet):

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Buttons list', LanguageReadSerializer(many=True)),
        },
        tags=['Components__Languages']
    )
    def list(self, request):
        """ Method returns all buttons """
        models = Language.objects.all()
        serializer = LanguageReadSerializer(models, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=LanguageCreateSerializer,
        responses={
            200: openapi.Response('Texts list', LanguageReadSerializer),
        },
        tags=['Components__Languages']
    )
    def create(self, request):
        serializer = LanguageCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_model = serializer.create(serializer.validated_data)
            new_serializer = LanguageReadSerializer(new_model)
            return Response(new_serializer.data, status=200)

    @swagger_auto_schema(
        request_body=LanguageUpdateSerializer,
        responses={
            200: openapi.Response('Texts list', LanguageReadSerializer),
        },
        tags=['Components__Languages']
    )
    def update(self, request, pk=None):
        serializer = LanguageUpdateSerializer(data=request.data)
        instance = get_object_or_404(Language, pk=pk)
        if serializer.is_valid():
            new_instance = serializer.update(instance=instance, validated_data=serializer.validated_data)
            new_serializer = LanguageReadSerializer(new_instance)
            return Response(new_serializer.data, status=200)

    @swagger_auto_schema(
        tags=['Components__Languages']
    )
    def destroy(self, request, pk=None):
        instance = get_object_or_404(Language, id=pk)
        instance.delete()
        return Response(status=200)

    @swagger_auto_schema(
        tags=['Components__Languages']
    )
    @action(methods=["get"], detail=False)
    def get_choices(self, request):
        lang_list = []
        if hasattr(settings, "LANG_CHOICES"):
            lang_list = [
                {
                    "label": lang[0],
                    "name": lang[1]
                 }
                for lang in settings.LANG_CHOICES
            ]
        return Response(lang_list, status=200)
