from rest_framework import serializers

from .models import ShortURL


class ShortURLCreateSerializer(serializers.Serializer):

    original_url = serializers.URLField()


class ShortURLSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShortURL

        fields = [
            "id",
            "original_url",
            "short_code",
            "created_at"
        ]

