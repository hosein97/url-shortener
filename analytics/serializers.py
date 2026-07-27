from rest_framework import serializers

class DashboardSerializer(
    serializers.Serializer
):

    total_links = serializers.IntegerField()

    total_clicks = serializers.IntegerField()

    recent_clicks = serializers.IntegerField()