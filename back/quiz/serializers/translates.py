from rest_framework import serializers
from ..models import MessageTranslation, QButtonTranslation


class MessageTranslateReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageTranslation
        fields = "__all__"


class MessageTranslateCreateSerializer(serializers.Serializer):

    language_id = serializers.IntegerField(required=True)
    message_id = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True)

    def create(self, validated_data):
        return MessageTranslation.objects.create(
            **validated_data
        )


class MessageTranslateUpdateSerializer(serializers.Serializer):

    text = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance


class ButtonTranslateReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = QButtonTranslation
        fields = "__all__"


class ButtonTranslateCreateSerializer(serializers.Serializer):

    language_id = serializers.IntegerField(required=True)
    button_id = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True)

    def create(self, validated_data):
        return QButtonTranslation.objects.create(
            **validated_data
        )


class ButtonTranslateUpdateSerializer(serializers.Serializer):

    text = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance
