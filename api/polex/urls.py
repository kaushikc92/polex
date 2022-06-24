from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/files/', include('filemgr.urls')),
    path('api/map/', include('mapmgr.urls')),
    path('api/query/', include('querymgr.urls')),
    path('admin/', admin.site.urls),
]
