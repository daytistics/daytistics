from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.middleware.csrf import get_token


class CsrfToken(APIView):
	def get(self, request, format=None):
		csrf_token = get_token(request)
		return Response({'csrfToken': csrf_token})
