from django.db import models
from filemgr.models import Document

# Create your models here.
class TiledDocument(models.Model):
     document = models.ForeignKey(Document, on_delete=models.CASCADE)
     subtable_number = models.IntegerField()
     tile_count_on_x = models.IntegerField()
     tile_count_on_y = models.IntegerField()
     total_tile_count = models.IntegerField()
