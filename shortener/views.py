from django.shortcuts import redirect
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from config.messaging.rabbitmq import publish_click

from shortener.serializers import ShortURLSerializer, ShortURLCreateSerializer
from shortener.services import get_user_links, create_short_url, get_original_url, get_short_url

from analytics.services import register_link

class CreateShortURLView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ShortURLCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        owner = (
            request.user
            if request.user.is_authenticated
            else None
        )
        
        short_url = create_short_url(
            original_url=serializer.validated_data[
                "original_url"
            ],
            owner=owner,
        )
        
        if owner:
            register_link(
                short_code=short_url.short_code,
                owner_id=owner.id,
                created_at=short_url.created_at,
            )
            
        response_serializer = ShortURLSerializer(
            short_url
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
        
        
class RedirectShortURLView(APIView):

    def get(self, request, short_code):
            
        original_url = get_original_url(short_code)

        publish_click(
            {
                "short_code": short_code,
                "ip_address": request.META.get("REMOTE_ADDR"),
                "user_agent": request.META.get("HTTP_USER_AGENT"),
                "referrer": request.META.get("HTTP_REFERER"),
            }
        ) 
                    
        return redirect(
            original_url
        )

        
        

class ListShortURLView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        links = get_user_links(
            user=request.user,
        )

        serializer = ShortURLSerializer(
            links,
            many=True,
        )

        return Response(serializer.data)
    
    
    
class RetrieveShortURLView(APIView):

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        short_url_id,
    ):

        short_url = get_short_url(
            short_url_id=short_url_id,
            owner=request.user,
        )
        
        serializer = ShortURLSerializer(
            short_url,
        )

        return Response(serializer.data)