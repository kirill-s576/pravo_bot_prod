from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..models import CustomUser
from ..serializers import CustomUserFullReadSerializer
from ..serializers import CustomUserCreateSerializer
from ..serializers import CustomUserUpdateSerializer


class CustomUserViewSet(ViewSet):

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=CustomUserCreateSerializer,
        responses={
            200: openapi.Response('response description', CustomUserFullReadSerializer)
        },
        tags=['Users']
    )
    @action(methods=["post"], detail=False)
    def registration(self, request):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            return Response({}, status=200)
        else:
            return Response({}, status=500)

    @swagger_auto_schema(
        operation_description="This method returns data for your authenticated user.",
        permission_classes=[IsAuthenticated],
        responses={
            200: openapi.Response('response description', CustomUserFullReadSerializer),
        },
        tags=['Users']
    )
    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def mine_get(self, request):
        serializer = CustomUserFullReadSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="This method updates data for your authenticated user.",
        permission_classes=[IsAuthenticated],
        request_body=CustomUserUpdateSerializer,
        responses={
            200: openapi.Response('response description', CustomUserFullReadSerializer)
        },
        tags=['Users']
    )
    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def mine_update(self, request):
        return Response({}, status=500)