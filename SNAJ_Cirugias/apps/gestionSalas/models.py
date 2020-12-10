from django.db import models

# Create your models here.

class Sala(models.Model):

    class Meta:
        db_table = 'Sala'

    idSala = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)
    lugar = models.CharField(max_length=100)