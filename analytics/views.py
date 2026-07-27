from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response

from analytics.serializers import (
    DashboardSerializer, TimeSeriesSerializer, TopLinkSerializer
)

from analytics.services import get_dashboard, get_click_timeseries, get_top_links

class DashboardView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        dashboard = get_dashboard(
            owner_id=request.user.id,
        )

        serializer = DashboardSerializer(
            dashboard,
        )

        return Response(serializer.data)
    
    


class ClickTimeSeriesView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        days = int(
            request.query_params.get(
                "days",
                30,
            )
        )

        data = get_click_timeseries(
            owner_id=request.user.id,
            days=days,
        )

        serializer = TimeSeriesSerializer(
            data,
            many=True,
        )

        return Response(serializer.data)
    
    
class TopLinksView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        links = get_top_links(
            owner_id=request.user.id,
        )

        serializer = TopLinkSerializer(
            links,
            many=True,
        )

        return Response(serializer.data)