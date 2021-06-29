from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Message
from ..serializers import (
    MessageReadSerializer,
    MessageRetrieveSerializer,
    MessageCreateSerializer,
    MessageUpdateSerializer,
    MessageTranslateReadSerializer
)


class MessageViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Texts list', MessageReadSerializer(many=True)),
        },
        tags=['Components__Texts']
    )
    def list(self, request):
        """ Method returns all texts """
        models = Message.objects.all()
        serializer = MessageReadSerializer(models, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=MessageCreateSerializer,
        responses={
            200: openapi.Response('Texts list', MessageReadSerializer),
        },
        tags=['Components__Texts']
    )
    def create(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_model = serializer.create(serializer.validated_data)
            new_serializer = MessageReadSerializer(new_model)
            return Response(new_serializer.data, status=200)

    @swagger_auto_schema(
        request_body=MessageUpdateSerializer,
        responses={
            200: openapi.Response('Texts list', MessageReadSerializer),
        },
        tags=['Components__Texts']
    )
    def update(self, request, pk=None):
        serializer = MessageUpdateSerializer(data=request.data)
        instance = get_object_or_404(Message, pk=pk)
        if serializer.is_valid():
            new_instance = serializer.update(instance=instance, validated_data=serializer.validated_data)
            new_serializer = MessageReadSerializer(new_instance)
            return Response(new_serializer.data, status=200)

    @swagger_auto_schema(
        tags=['Components__Texts']
    )
    def destroy(self, request, pk=None):
        instance = get_object_or_404(Message, pk=pk)
        instance.delete()
        return Response(status=200)

    @swagger_auto_schema(
        tags=['Components__Texts']
    )
    @action(methods=["GET"], detail=True)
    def get_translates(self, request, pk=None):
        instance = get_object_or_404(Message, pk=pk)
        translates = instance.get_translates()
        serializer = MessageTranslateReadSerializer(translates, many=True)
        return Response(serializer.data, status=200)