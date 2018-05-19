from django.db import models

class Top(models.Model):
    top_name = models.CharField(max_length=20)
    top_value = models.FloatField()

class Weight(models.Model):
    top_name = models.CharField(max_length=20)
    weight_value = models.FloatField()

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
