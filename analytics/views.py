from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.serializers import (
    DashboardSerializer,
    TimeSeriesSerializer,
    TopLinkSerializer,
    LinkDashboardSerializer,
)

from analytics.services import (
    dashboard,
    click_timeseries,
    top_links,
    links_dashboard,
)

class DashboardView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        data = dashboard(
            owner_id=request.user.id,
        )

        serializer = DashboardSerializer(data)

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

        data = click_timeseries(
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

        data = top_links(
            owner_id=request.user.id,
        )

        serializer = TopLinkSerializer(
            data,
            many=True,
        )

        return Response(serializer.data)
    
    

class LinksDashboardView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):

        page = int(
            request.query_params.get(
                "page",
                1,
            )
        )

        page_size = int(
            request.query_params.get(
                "page_size",
                20,
            )
        )

        data = links_dashboard(
            owner_id=request.user.id,
            page=page,
            page_size=page_size,
        )

        serializer = LinkDashboardSerializer(
            data,
            many=True,
        )

        return Response(serializer.data)