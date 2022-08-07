from django.conf import settings
from django.core.files import File

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

import string, random

from filemgr.models import Document
from mapmgr.views import convert_html

class ExecuteQuery(APIView):
    parser_class = (JSONParser,)

    def post(self, request):
        query = request.data['query']
        uid = request.data['uid']
        
        query_uid = "".join(random.choices(string.ascii_lowercase + string.digits,k=10))
        query_path = "{0}.csv".format(query_uid)
        path = "{0}/documents/{1}.csv".format(settings.MEDIA_ROOT, uid)
        if "SELECT" in query or "select" in query:
            exec(
                "import pandas as pd\n" +
                "import pandasql as ps\n" +
                "df = pd.read_csv('" + path + "')\n" +
                "of = ps.sqldf('" + query + "')\n" +
                "of.to_csv('" + query_path + "', index=False)"
            )
        else:
            exec(
                "import pandas as pd\n" +
                "df = pd.read_csv('" + path + "')\n" +
                "of =" + query + "\n" +
                "of.to_csv('" + query_path + "', index=False)"
            )
        newDoc = Document(
            uid=query_uid,
            file_name="{0}.csv".format(query_uid),
            docfile=File(open(query_path, 'r')),
            rows=0,
            columns=0
        )
        newDoc.docfile.name = "{0}.csv".format(query_uid)
        newDoc.save()
        convert_html(newDoc)

        return Response(status=status.HTTP_200_OK)
