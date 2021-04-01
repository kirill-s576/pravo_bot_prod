from rest_framework import serializers


class StatisticRequestSerializer(serializers.Serializer):

    stat_from = serializers.DateField(required=True)
    stat_to = serializers.DateField(required=True)