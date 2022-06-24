from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FileUploadParser

class UploadFile(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request):
        return Response(status=status.HTTP_200_OK)
