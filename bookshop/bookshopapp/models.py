from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class Zanr(models.Model):
    naziv = models.CharField(max_length = 50)

class Autor(models.Model):
    ime = models.CharField(max_length = 50)
    prezime = models.CharField(max_length = 50)

class Artikl(models.Model):
    naziv = models.CharField(max_length = 50)
    cijena = models.FloatField()
    opis = models.CharField(max_length = 256)
    slika = models.ImageField(default='')
    zanr = models.ForeignKey(Zanr, on_delete=models.CASCADE)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)

class Kosarica(models.Model):
    ukupnaCijena = models.FloatField()
    artikli = models.ManyToManyField(Artikl)

class Recenzija(models.Model):
    ocjena = models.IntegerField(null=True)
    komentar = models.CharField(max_length = 500)
    artikl = models.ForeignKey(Artikl, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)