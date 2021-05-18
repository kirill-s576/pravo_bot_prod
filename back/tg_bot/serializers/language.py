from rest_framework import serializers
from ..models import Language


class BotLanguageListSerializer(serializers.Serializer):
    """Serializer for Language List view"""

    id = serializers.IntegerField(read_only=True)
    label = serializers.CharField(max_length=10, required=True)
    name = serializers.CharField(max_length=255, required=True)
    is_active = serializers.BooleanField()

class BotLanguageCreateSerializer(serializers.Serializer):
    """Serializer for Language Create view"""

    label = serializers.CharField(max_length=10, required=True)
    name = serializers.CharField(max_length=255, required=True)

    def create(self, validated_data):
        return Language.objects.create(**validated_data)


class BotLanguageUpdateSerializer(serializers.Serializer):
    """Serializer for Language Update view"""

    label = serializers.CharField(max_length=10, required=False)
    name = serializers.CharField(max_length=255, required=False)
    is_active = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):
        instance.label = validated_data.get("label", instance.label)
        instance.name = validated_data.get("name", instance.name)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance