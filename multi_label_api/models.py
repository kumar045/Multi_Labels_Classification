from django.db import models
# Create your models here.

class MultiLabel(models.Model):
    path_of_folder = models.CharField(max_length=3000)