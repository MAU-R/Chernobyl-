from django.db import models


class franquicias(models.Model):
    Color=models.CharField(max_length=200)
    Nombre=models.CharField(max_length=200)
    Descripcion=models.CharField(max_length=100)
    latitud=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)