from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FileUploadParser

from pymongo import MongoClient

import string, random

class UploadFile(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request):
        f = request.data["file"]
        file_name = request.data["fileName"]
        uid = "".join(random.choices(string.ascii_lowercase + string.digits,k=10))
        with open(settings.MEDIA_ROOT + "/files/" + uid + ".csv", "wb+") as fout:
            fout.write(f.read())
        mongo_client = MongoClient("mongodb://localhost:27017/")
        db = mongo_client["polex"]
        files_collection = db["files"]
        file_doc = {
            "uid": uid,
            "name": file_name
        }
        files_collection.insert_one(file_doc)

        return Response(status=status.HTTP_200_OK)

class ListFiles(APIView):
    parser_class = (JSONParser,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
