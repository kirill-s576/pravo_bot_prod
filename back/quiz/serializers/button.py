from rest_framework import serializers
from ..models import QButton


class ButtonReadSerializer(serializers.Serializer):
    """"""
    id = serializers.IntegerField(required=True)
    default_text = serializers.CharField(max_length=255, required=True)


class ButtonCreateSerializer(serializers.Serializer):

    default_text = serializers.CharField(max_length=255, required=True)

    def create(self, validated_data):
        return QButton.objects.create(**validated_data)


class ButtonUpdateSerializer(serializers.Serializer):

    default_text = serializers.CharField(max_length=255, required=False)

    def update(self, instance, validated_data):
        instance.default_text = validated_data.get("default_text", instance.default_text)
        instance.save()
        return instance