from rest_framework import serializers


class OptionalFieldSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    required = serializers.BooleanField(default=True)
    label = serializers.CharField(required=True)


class SuccessResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField(label="success message")

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()