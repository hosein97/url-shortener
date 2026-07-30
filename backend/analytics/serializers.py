from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):

    total_links = serializers.IntegerField()

    total_clicks = serializers.IntegerField()

    clicks_today = serializers.IntegerField()

    clicks_last_7_days = serializers.IntegerField()

    unique_visitors = serializers.IntegerField()


class TimeSeriesSerializer(serializers.Serializer):

    date = serializers.DateField()

    clicks = serializers.IntegerField()


class TopLinkSerializer(serializers.Serializer):

    short_code = serializers.CharField()

    original_url = serializers.URLField()

    clicks = serializers.IntegerField()

    last_click = serializers.DateTimeField()


class LinkDashboardSerializer(serializers.Serializer):

    short_code = serializers.CharField()

    original_url = serializers.URLField()

    created_at = serializers.DateTimeField()

    clicks = serializers.IntegerField()

    unique_visitors = serializers.IntegerField()

    last_click = serializers.DateTimeField(
        allow_null=True,
    )