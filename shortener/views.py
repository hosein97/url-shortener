from django.shortcuts import redirect
from django.http import Http404
from django.db.models import F


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config.messaging.rabbitmq import publish_click

from .models import ShortURL
from .serializers import (
    ShortURLCreateSerializer,
    ShortURLResponseSerializer
)
from .services import create_short_url, increment_clicks, get_original_url


class CreateShortURLView(APIView):

    def post(self, request):

        serializer = ShortURLCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        short_url = create_short_url(
            original_url=serializer.validated_data[
                "original_url"
            ]
        )

        response_serializer = (
            ShortURLResponseSerializer(short_url)
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class RedirectShortURLView(APIView):

    def get(self, request, short_code):

        try:
            
            original_url = get_original_url(short_code)

            publish_click(short_code)
            
            return redirect(
                original_url
            )

        except ShortURL.DoesNotExist:
            raise Http404("Short URL not found")