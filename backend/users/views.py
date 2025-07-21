from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView

class UsersAPIView(APIView):
    def get(self, request, id=None):
        return Response('norm', status=200)
