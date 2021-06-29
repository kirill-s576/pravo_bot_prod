from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import MessageTranslation, QButtonTranslation
from ..serializers import (
    MessageTranslateReadSerializer,
    MessageTranslateUpdateSerializer,
    MessageTranslateCreateSerializer
)
from ..serializers import (
    ButtonTranslateReadSerializer,
    ButtonTranslateCreateSerializer,
    ButtonTranslateUpdateSerializer
)


class MessageTranslationViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Texts list', MessageTranslateReadSerializer(many=True)),
        },
        tags=['Translates__Message']
    )
    def list(self, request):
        """ Method returns all texts """
        models = MessageTranslation.objects.all()
        serializer = MessageTranslateReadSerializer(models, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=MessageTranslateCreateSerializer,
        responses={
            200: openapi.Response('Texts list', MessageTranslateReadSerializer),
        },
        tags=['Translates__Message']
    )
    def create(self, request):
        serializer = MessageTranslateCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_model = serializer.create(serializer.validated_data)
            new_serializer = MessageTranslateReadSerializer(new_model)
            return Response(new_serializer.data, status=200)

    @swagger_auto_schema(
        request_body=MessageTranslateUpdateSerializer,
        responses={
            200: openapi.Response('Texts list', MessageTranslateReadSerializer),
        },
        tags=['Translates__Message']
    )
    def update(self, request, pk=None):
        serializer = MessageTranslateUpdateSerializer(data=request.data)
        instance = get_object_or_404(MessageTranslation, pk=pk)
        if serializer.is_valid():
            new_instance = serializer.update(instance=instance, validated_data=serializer.validated_data)
            new_serializer = MessageTranslateReadSerializer(new_instance)
            return Response(new_serializer.data, status=200)

    @swagger_auto_schema(
        tags=['Translates__Message']
    )
    def destroy(self, request, pk=None):
        instance = get_object_or_404(MessageTranslation, pk=pk)
        instance.delete()
        return Response(status=200)


class QButtonTranslationViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Texts list', ButtonTranslateReadSerializer(many=True)),
        },
        tags=['Translates__Buttons']
    )
    def list(self, request):
        """ Method returns all texts """
        models = QButtonTranslation.objects.all()
        serializer = ButtonTranslateReadSerializer(models, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=ButtonTranslateCreateSerializer,
        responses={
            200: openapi.Response('Texts list', ButtonTranslateReadSerializer),
        },
        tags=['Translates__Buttons']
    )
    def create(self, request):
        serializer = ButtonTranslateCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_model = serializer.create(serializer.validated_data)
            new_serializer = ButtonTranslateReadSerializer(new_model)
            return Response(new_serializer.data, status=200)

    @swagger_auto_schema(
        request_body=ButtonTranslateUpdateSerializer,
        responses={
            200: openapi.Response('Texts list', ButtonTranslateReadSerializer),
        },
        tags=['Translates__Buttons']
    )
    def update(self, request, pk=None):
        serializer = ButtonTranslateUpdateSerializer(data=request.data)
        instance = get_object_or_404(QButtonTranslation, pk=pk)
        if serializer.is_valid():
            new_instance = serializer.update(instance=instance, validated_data=serializer.validated_data)
            new_serializer = ButtonTranslateReadSerializer(new_instance)
            return Response(new_serializer.data, status=200)

    @swagger_auto_schema(
        tags=['Translates__Buttons']
    )
    def destroy(self, request, pk=None):
        instance = get_object_or_404(QButtonTranslation, pk=pk)
        instance.delete()
        return Response(status=200)