from django.urls import path
from .views import CreateShortURLView, RedirectShortURLView

urlpatterns = [
    path(
        "shorten/",
        CreateShortURLView.as_view()
    ),
    path(
        "<str:short_code>/",
        RedirectShortURLView.as_view()
    ),
    
]