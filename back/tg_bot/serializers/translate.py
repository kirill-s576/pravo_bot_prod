from rest_framework import serializers
from ..models import MessageTranslate


class BotMessageTranslateListSerializer(serializers.Serializer):
    """Serializer for translate List view"""

    id = serializers.IntegerField(allow_null=False)
    language_id = serializers.PrimaryKeyRelatedField(allow_null=False, read_only=True)
    message_id = serializers.PrimaryKeyRelatedField(allow_null=False, read_only=True)
    text = serializers.CharField(required=True, allow_null=False)


class BotMessageTranslateCreateSerializer(serializers.Serializer):
    """Serializer for translate create view"""

    language_id = serializers.IntegerField(allow_null=False)
    message_id = serializers.IntegerField(allow_null=False)
    text = serializers.CharField(required=True, allow_null=False)

    def create(self, validated_data):
        return MessageTranslate.objects.create(**validated_data)


class BotMessageTranslateUpdateSerializer(serializers.Serializer):
    """Serializer for translate update view"""

    text = serializers.CharField(required=False, allow_null=False)

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance