from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404

from ..models import MessageTranslate
from ..serializers import (
    BotMessageTranslateListSerializer,
    BotMessageTranslateCreateSerializer,
    BotMessageTranslateUpdateSerializer
)

class BotTranslateViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Languages list', BotMessageTranslateListSerializer(many=True)),
        },
        tags=['Bot__Translates']
    )
    def list(self, request):
        """ Method returns all available languages """
        models = MessageTranslate.objects.all()
        serializer = BotMessageTranslateListSerializer(models, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=BotMessageTranslateCreateSerializer,
        responses={
            200: openapi.Response('Created language', BotMessageTranslateListSerializer),
        },
        tags=['Bot__Translates']
    )
    def create(self, request):
        serializer = BotMessageTranslateCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_model = serializer.create(serializer.validated_data)
            new_serializer = BotMessageTranslateListSerializer(new_model)
            return Response(new_serializer.data, status=200)
        else:
            return Response({"error": "Serializer isn't valid"}, status=400)

    @swagger_auto_schema(
        request_body=BotMessageTranslateUpdateSerializer,
        responses={
            200: openapi.Response('Updated Language', BotMessageTranslateListSerializer),
        },
        tags=['Bot__Translates']
    )
    def update(self, request, pk=None):
        serializer = BotMessageTranslateUpdateSerializer(data=request.data)
        instance = get_object_or_404(MessageTranslate, pk=pk)
        if serializer.is_valid():
            new_instance = serializer.update(instance=instance, validated_data=serializer.validated_data)
            new_serializer = BotMessageTranslateListSerializer(new_instance)
            return Response(new_serializer.data, status=200)
        else:
            return Response({"error": "Serializer isn't valid"}, status=400)

    @swagger_auto_schema(
        tags=['Bot__Translates']
    )
    def destroy(self, request, pk=None):
        instance = get_object_or_404(MessageTranslate, pk=pk)
        instance.delete()
        return Response(status=200)