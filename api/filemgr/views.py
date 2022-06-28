from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FileUploadParser

import string, random, os, shutil

from filemgr.models import Document
from mapmgr.views import convert_html

class UploadFile(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request):
        f = request.data["file"]
        file_name = request.data["fileName"]
        uid = "".join(random.choices(string.ascii_lowercase + string.digits,k=10))

        newDoc = Document(
            uid=uid,
            file_name=file_name,
            docfile=f,
            rows=0,
            columns=0
        )
        newDoc.docfile.name = "{0}.csv".format(uid)
        newDoc.save()
        convert_html(newDoc)

        return Response(status=status.HTTP_200_OK)

class ListFiles(APIView):
    parser_class = (JSONParser,)

    def get(self, request):
        docs = []
        for doc in Document.objects.all():
            docs.append({
                "uid": doc.uid,
                "name": doc.file_name
            })
        return Response(docs, status=status.HTTP_200_OK)

class DeleteFile(APIView):
    parser_class = (JSONParser,)

    def post(self, request):
        uid = request.data["uid"]
        Document.objects.get(uid=uid).delete()
        os.remove("{0}/documents/{1}.csv".format(settings.MEDIA_ROOT, uid))
        shutil.rmtree("{0}/tiles/{1}".format(settings.MEDIA_ROOT, uid))

        return Response(status=status.HTTP_200_OK) 
