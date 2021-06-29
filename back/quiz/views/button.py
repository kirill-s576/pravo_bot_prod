from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import QButton
from ..serializers import (
    ButtonReadSerializer,
    ButtonCreateSerializer,
    ButtonUpdateSerializer,
    ButtonTranslateReadSerializer
)


class QButtonViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Buttons list', ButtonReadSerializer(many=True)),
        },
        tags=['Components__Buttons']
    )
    def list(self, request):
        """ Method returns all buttons """
        models = QButton.objects.all()
        serializer = ButtonReadSerializer(models, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=ButtonCreateSerializer,
        responses={
            200: openapi.Response('Texts list', ButtonReadSerializer),
        },
        tags=['Components__Buttons']
    )
    def create(self, request):
        serializer = ButtonCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_model = serializer.create(serializer.validated_data)
            new_serializer = ButtonReadSerializer(new_model)
            return Response(new_serializer.data, status=200)

    @swagger_auto_schema(
        request_body=ButtonUpdateSerializer,
        responses={
            200: openapi.Response('Texts list', ButtonReadSerializer),
        },
        tags=['Components__Buttons']
    )
    def update(self, request, pk=None):
        serializer = ButtonUpdateSerializer(data=request.data)
        instance = get_object_or_404(QButton, pk=pk)
        if serializer.is_valid():
            new_instance = serializer.update(instance=instance, validated_data=serializer.validated_data)
            new_serializer = ButtonReadSerializer(new_instance)
            return Response(new_serializer.data, status=200)

    @swagger_auto_schema(
        tags=['Components__Buttons']
    )
    def destroy(self, request, pk=None):
        instance = get_object_or_404(QButton, id=pk)
        instance.delete()
        return Response(status=200)

    @swagger_auto_schema(
        tags=['Components__Texts']
    )
    @action(methods=["GET"], detail=True)
    def get_translates(self, request, pk=None):
        instance = get_object_or_404(QButton, pk=pk)
        translates = instance.get_translates()
        serializer = ButtonTranslateReadSerializer(translates, many=True)
        return Response(serializer.data, status=200)