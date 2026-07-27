from django.urls import path

from analytics.views import DashboardView, ClickTimeSeriesView, TopLinksView

urlpatterns = [
    path(
        "me/dashboard/",
        DashboardView.as_view(),
    ),
    path(
    "me/clicks/timeseries/",
    ClickTimeSeriesView.as_view(),
    ),
    path(
        "me/top-links/",
        TopLinksView.as_view(),
    ),
]


