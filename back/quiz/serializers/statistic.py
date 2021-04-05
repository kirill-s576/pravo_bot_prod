from rest_framework import serializers


class StatisticRequestSerializer(serializers.Serializer):

    date_from = serializers.DateField(required=True)
    date_to = serializers.DateField(required=True)

