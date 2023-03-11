from django.db import models
from Centro_de_custo.models import CentroCusto

# Create your models here.

class Etapas(models.Model):
    id_etapa = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    etapa = models.CharField(max_length=60, blank=True, null=True)
    id_cc = models.ForeignKey(CentroCusto, models.DO_NOTHING, db_column='id_cc')

    class Meta:
        managed = True
        ordering = ['etapa']
        db_table = 'etapas'
