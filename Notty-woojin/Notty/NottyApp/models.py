from django.db import models

# Create your models here.
class Route(models.Model):
    start = models.CharField(max_length=30)
    fin = models.CharField(max_length=30)
    
