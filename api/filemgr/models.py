from django.db import models

# Create your models here.
class Document(models.Model):
    uid = models.CharField(max_length=20)
    file_name = models.CharField(max_length=200)
    docfile = models.FileField(upload_to='documents/')
    last_access = models.DateTimeField(auto_now=True)
    rows = models.IntegerField()
    columns = models.IntegerField()
