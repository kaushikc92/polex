from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.core.files.base import ContentFile

from tempfile import TemporaryFile
from tiler.forms import DocumentForm
from tiler.models.Document import Document
import os, requests

def file_with_same_name_exists(request):
    return HttpResponse(False)

def file_exists_in_db(file_name):
    """
    Check if file already exists in database
    Args:
        file_name
    Returns:
        True if file exists, else False
    """
    docs = Document.objects.filter(file_name=file_name)
    if not docs:
        return False
    else:
        return True

@method_decorator(csrf_exempt)
def list_files(request):
    """
    Request handler for listing csv files on the index page. Handles GET requests used for listing all the
    files and POST requests for adding a new file.
    Args:
        request: The HTTP request object.
    Returns: HTTP response object that contains html for the index page in case of GET request. Redirects to
    the csv viewer page in case of POST request.
    """
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid() and not file_exists_in_db(request.FILES['docfile'].name):
            newdoc = Document(file_name=request.FILES['docfile'].name, docfile=request.FILES['docfile'],
                rows=0, columns=0)
            newdoc.save()
            return redirect('map/leaflet?file=' + request.FILES['docfile'].name)
    else:
        form = DocumentForm()
    documents = Document.objects.all()
    return render(request, 'list.html', {'documents': documents, 'form': form})

@method_decorator(csrf_exempt)
def import_cdrive_file(request):
    download_url = request.POST['download_url']
    file_name = request.POST['file_name']

    response = requests.get(download_url)

    with TemporaryFile() as tf:
        tf.write(response.content)
        newdoc = Document(file_name=file_name, rows=0, columns=0)
        newdoc.docfile.save(file_name, File(tf))
        newdoc.save()

    return redirect('../map/leaflet?file=' + file_name)

def client_id(request):
    client_id = os.environ['COLUMBUS_CLIENT_ID']
    return JsonResponse({'clientId': client_id})

@method_decorator(csrf_exempt)
def access_token(request):
    code = request.POST['code']
    redirect_uri = request.POST['redirect_uri']
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': os.environ['COLUMBUS_CLIENT_ID'],
        'client_secret': os.environ['COLUMBUS_CLIENT_SECRET']
    }
    response = requests.post(url='http://authentication.dev1.columbustech.io/o/token/', data=data)

    return JsonResponse(response.json())
