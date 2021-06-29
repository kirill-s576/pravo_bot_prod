from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from ..models import Message
from ..serializers import (
    BotMessageListSerializer,
    BotMessageCreateSerializer,
    BotMessageUpdateSerializer,
    BotMessageTranslateListSerializer
)

class BotMessageViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Languages list', BotMessageListSerializer(many=True)),
        },
        tags=['Bot__Messages']
    )
    def list(self, request):
        """ Method returns all available languages """
        models = Message.objects.all()
        serializer = BotMessageListSerializer(models, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=BotMessageCreateSerializer,
        responses={
            200: openapi.Response('Created language', BotMessageListSerializer),
        },
        tags=['Bot__Messages']
    )
    def create(self, request):
        serializer = BotMessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_model = serializer.create(serializer.validated_data)
            new_serializer = BotMessageListSerializer(new_model)
            return Response(new_serializer.data, status=200)
        else:
            return Response({"error": "Serializer isn't valid"}, status=400)

    @swagger_auto_schema(
        request_body=BotMessageUpdateSerializer,
        responses={
            200: openapi.Response('Updated Language', BotMessageListSerializer),
        },
        tags=['Bot__Messages']
    )
    def update(self, request, pk=None):
        serializer = BotMessageUpdateSerializer(data=request.data)
        instance = get_object_or_404(Message, pk=pk)
        if serializer.is_valid():
            new_instance = serializer.update(instance=instance, validated_data=serializer.validated_data)
            new_serializer = BotMessageListSerializer(new_instance)
            return Response(new_serializer.data, status=200)
        else:
            return Response({"error": "Serializer isn't valid"}, status=400)

    @swagger_auto_schema(
        tags=['Bot__Messages']
    )
    def destroy(self, request, pk=None):
        instance = get_object_or_404(Message, pk=pk)
        instance.delete()
        return Response(status=200)

    @swagger_auto_schema(
        tags=['Bot__Messages']
    )
    @action(methods=["GET"], detail=True)
    def get_translates(self, request, pk=None):
        instance = get_object_or_404(Message, pk=pk)
        translates = instance.translates
        serializer = BotMessageTranslateListSerializer(translates, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        tags=['Bot__Messages']
    )
    @action(methods=["POST"], detail=True)
    def get_translate_by_language_id(self, request, pk=None):
        instance = get_object_or_404(Message, pk=pk)
        language_id = request.data.get("language_id", None)
        if not language_id:
            raise ValidationError('language_id required', code='language_id')
        translate = instance.get_translate_by_language_id(int(language_id))
        serializer = BotMessageTranslateListSerializer(translate)
        return Response(serializer.data, status=200)