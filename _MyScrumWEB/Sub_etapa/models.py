from django.db import models
from Etapa.models import Etapas
# Create your models here.

class SubEtapas(models.Model):
    id_sub_etapas = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    sub_etapa = models.CharField(max_length=45, blank=True, null=True)
    id_etapa = models.ForeignKey(Etapas, models.DO_NOTHING, db_column='id_etapa')

    class Meta:
        managed = True
        ordering = ['sub_etapa']
        db_table = 'sub_etapas'
