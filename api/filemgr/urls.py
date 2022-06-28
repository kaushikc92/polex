from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.UploadFile.as_view()),
    path('list/', views.ListFiles.as_view()),
    path('delete/', views.DeleteFile.as_view())
]

