from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):

    total_links = serializers.IntegerField()

    total_clicks = serializers.IntegerField()

    clicks_today = serializers.IntegerField()

    clicks_last_7_days = serializers.IntegerField()
    
    


class TimeSeriesSerializer(
    serializers.Serializer
):

    date = serializers.DateField()

    clicks = serializers.IntegerField()
    


class TopLinkSerializer(
    serializers.Serializer
):

    short_code = serializers.CharField()

    clicks = serializers.IntegerField()

    last_click = serializers.DateTimeField()