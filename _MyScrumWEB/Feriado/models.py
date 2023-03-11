from django.db import models

# Create your models here.

class Feriados(models.Model):
    id_feriado = models.AutoField(primary_key=True)
    data_feriado = models.DateField(blank=True, null=True)
    descri_feriado = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feriados'