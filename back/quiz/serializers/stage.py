from rest_framework import serializers
from ..models import Stage, Message
from .message import MessageReadSerializer
from .button import ButtonReadSerializer
from .message import MessageRetrieveSerializer


class StageReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stage
        fields = "__all__"

class StageShortSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    button = ButtonReadSerializer()


class StageRetrieveSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    button = ButtonReadSerializer()
    title = serializers.CharField()
    question = MessageRetrieveSerializer()
    messages = MessageRetrieveSerializer(many=True)
    children = StageShortSerializer(many=True)


class StageCreateSerializer(serializers.Serializer):

    to_stage_id = serializers.IntegerField(required=True)
    button_id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True)

    def create(self, validated_data):
        to_stage = Stage.objects.get(id=validated_data["to_stage_id"])
        new_stage = Stage.objects.create(title=validated_data["title"],
                                         button_id=validated_data["button_id"])
        to_stage.question.stages.add(new_stage)
        return new_stage


class StageUpdateSerializer(serializers.Serializer):
    pass