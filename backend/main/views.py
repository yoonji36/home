# django rest-framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage  # default_storage 임포트
from django.core.files.base import ContentFile
from django.utils import timezone
from django.core.cache import cache
from django.http import JsonResponse
import requests, os, logging

logger = logging.getLogger(__name__)

class WelcomeView(APIView):
    def get(self, request):
        user_id = request.user.id if request.user.is_authenticated else 'Guest'
        return Response({'message': f'Welcome, {user_id}!'}, status=status.HTTP_200_OK)
