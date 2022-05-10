from django.conf import settings
from django.conf.urls.static import static

"""magicktable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
                  path('', views.list_files, name='index'),
                  path('fileexists/', views.file_with_same_name_exists, name='file_exists'),
                  path('map/', include('mapui.urls')),
                  path('tiler/', include('tiler.urls')),
                  path('client-id/', views.client_id, name='client_id'),
                  path('access-token/', views.access_token, name='access_token'),
                  path('import-cdrive-file/', views.import_cdrive_file, name='import_cdrive_file'),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
