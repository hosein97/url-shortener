from django.urls import path
from .views import CreateShortURLView, RedirectShortURLView, ListShortURLView

urlpatterns = [
    path(
        "shorten/",
        CreateShortURLView.as_view()
    ),
    path(
        "links/",
        ListShortURLView.as_view(),
    ),    
    path(
        "<str:short_code>/",
        RedirectShortURLView.as_view(),
        name="redirect"
    ),
    
]