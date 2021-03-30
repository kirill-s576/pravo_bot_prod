from rest_framework import serializers
from ..models import Message


class MessageReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = "__all__"


class MessageRetrieveSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    title = serializers.CharField()
    default_text = serializers.CharField()
    is_hint = serializers.BooleanField()


class MessageCreateSerializer(serializers.Serializer):

    title = serializers.CharField(required=True)
    default_text = serializers.CharField(required=True)
    is_hint = serializers.BooleanField(required=False)

    def create(self, validated_data):
        return Message.objects.create(
            **validated_data
        )


class MessageUpdateSerializer(serializers.Serializer):

    title = serializers.CharField(required=False)
    default_text = serializers.CharField(required=False)
    is_hint = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.default_text = validated_data.get('default_text', instance.default_text)
        instance.is_hint = validated_data.get('is_hint', instance.is_hint)
        instance.save()
        return instance

