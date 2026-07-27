from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response

from analytics.serializers import (
    DashboardSerializer,
)
from analytics.services import (
    get_dashboard_stats,
)


class DashboardView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
    ):

        stats = get_dashboard_stats(
            user=request.user,
        )

        serializer = DashboardSerializer(
            stats,
        )

        return Response(
            serializer.data,
        )