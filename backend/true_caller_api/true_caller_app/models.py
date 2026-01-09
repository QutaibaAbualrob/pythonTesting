from django.db import models

# Create your models here.

class phone(models.Model):
    full_name = models.CharField(max_length=255)
    number = models.IntegerField()
        