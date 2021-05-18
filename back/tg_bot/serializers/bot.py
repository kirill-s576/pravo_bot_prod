from rest_framework import serializers


class SetWebhookSerializer(serializers.Serializer):
    """
    Serializer for SetWebhookUrl View
    """
    url = serializers.CharField(max_length=1024, required=True)