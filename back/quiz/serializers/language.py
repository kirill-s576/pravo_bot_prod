from rest_framework import serializers
from ..models import Language


class LanguageReadSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=True)
    label = serializers.CharField(max_length=255, required=True)
    name = serializers.CharField(max_length=255, required=True)


class LanguageCreateSerializer(serializers.Serializer):

    label = serializers.CharField(max_length=255, required=True)
    name = serializers.CharField(max_length=255, required=True)

    def create(self, validated_data):
        return Language.objects.create(**validated_data)


class LanguageUpdateSerializer(serializers.Serializer):

    label = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=False)

    def update(self, instance, validated_data):
        instance.label = validated_data.get("label", instance.label)
        instance.label = validated_data.get("name", instance.name)
        instance.save()
        return instance