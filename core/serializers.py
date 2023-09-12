"""Serializers."""
from rest_framework import serializers


class ResponseSerializer(serializers.Serializer):
    """Serializer for Response."""

    detail = serializers.CharField()


class ResponseCodeSerializer(serializers.Serializer):
    """Response Serializer for Code."""

    code = serializers.CharField()
    detail = serializers.CharField()
