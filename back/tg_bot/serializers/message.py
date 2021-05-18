from rest_framework import serializers
from ..models import Message


class BotMessageListSerializer(serializers.Serializer):
    """Serializer for message List view"""
    
    id = serializers.IntegerField(read_only=True)
    label = serializers.CharField(max_length=24, required=True, allow_null=False)
    text = serializers.CharField(required=True, allow_null=False)


class BotMessageCreateSerializer(serializers.Serializer):
    """Serializer for message Create view"""

    label = serializers.CharField(max_length=24, required=True, allow_null=False)
    text = serializers.CharField(required=True, allow_null=False)

    def create(self, validated_data):
        return Message.objects.create(**validated_data)


class BotMessageUpdateSerializer(serializers.Serializer):
    """Serializer for message Update view"""

    label = serializers.CharField(max_length=24, required=False, allow_null=False)
    text = serializers.CharField(required=False, allow_null=False)

    def update(self, instance, validated_data):
        instance.label = validated_data.get("label", instance.label)
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance