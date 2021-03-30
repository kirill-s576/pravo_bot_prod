from rest_framework import serializers


class CustomUserBaseSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False, allow_null=True)
    first_name = serializers.CharField(required=False, allow_null=True)
    last_name = serializers.CharField(required=False, allow_null=True)
    about = serializers.CharField(allow_null=True, required=False)


class CustomUserFullReadSerializer(CustomUserBaseSerializer):

    pass


class CustomUserCreateSerializer(CustomUserBaseSerializer):

    password = serializers.CharField(required=True)

    def create(self, validated_data):
        pass


class CustomUserUpdateSerializer(CustomUserBaseSerializer):

    def update(self, instance, validated_data):
        pass
