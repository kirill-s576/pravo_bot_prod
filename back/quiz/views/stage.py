from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Stage
from ..serializers import (
    StageCreateSerializer,
    StageReadSerializer,
    StageUpdateSerializer,
    StageRetrieveSerializer
)


class StageViewSet(ViewSet):

    queryset = Stage.objects.all()
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Texts list', StageReadSerializer(many=True)),
        },
        tags=['Stages']
    )
    def list(self, request):
        serializer = StageReadSerializer(self.queryset, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Texts list', StageRetrieveSerializer),
        },
        tags=['Stages']
    )
    def retrieve(self, request, pk=None):
        model = get_object_or_404(Stage, pk=pk)
        serializer = StageRetrieveSerializer(model)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=StageCreateSerializer,
        responses={
            200: openapi.Response('Texts list', StageReadSerializer),
        },
        tags=['Stages']
    )
    def create(self, request):
        serializer = StageCreateSerializer(data=request.data)
        if serializer.is_valid():
            new_instance = serializer.create(serializer.validated_data)
            new_serializer = StageReadSerializer(new_instance)
            return Response(new_serializer.data, status=200)
        return Response(status=500)

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Status 200 Response"),
        },
        tags=['Stages']
    )
    def destroy(self, request, pk=None):
        model = get_object_or_404(Stage, pk=pk)
        model.delete()
        return Response(status=200)

    @swagger_auto_schema(
        request_body=StageUpdateSerializer,
        responses={
            200: openapi.Response('Texts list', StageReadSerializer),
        },
        tags=['Stages']
    )
    def update(self, request, pk=None):
        instance = get_object_or_404(Stage, pk=pk)
        return Response({}, status=200)

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Stages tree..."),
        },
        tags=['Stages']
    )
    @action(methods=["GET"], detail=False)
    def tree(self, request):
        tree = Stage.get_tree(starts_with_id=30001)
        # import json
        # with open("/Users/kirill/own-projects/freelance/pravo_bot/dump_2.json", "r") as f:
        #     tree = json.loads(f.read())
        return Response(tree, status=200)

    @action(methods=["POST"], detail=True)
    def add_message(self, request, pk=None):
        pass

