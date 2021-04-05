from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Session
from ..serializers import StatisticRequestSerializer
from ..interface import PeriodSessionStatistic


class SessionViewSet(ViewSet):

    @swagger_auto_schema(
        request_body=StatisticRequestSerializer,
        responses={
            200: openapi.Response('Statistic'),
        },
        tags=['Sessions']
    )
    @action(methods=["POST"], detail=False)
    def get_statistic(self, request):
        serializer = StatisticRequestSerializer(data=request.data)
        if serializer.is_valid():
            stat_interface = PeriodSessionStatistic(
                date_from=serializer.validated_data["date_from"],
                date_to=serializer.validated_data["date_to"]
            )
            return Response(
                stat_interface.get_json(),
                status=200
            )