from django.db import models

# Create your models here.

class CentroCusto(models.Model):
    id_centro_custo = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    id_sienge = models.IntegerField(blank=True, null=True)
    centrocusto = models.CharField(max_length=45)

    class Meta:
        managed = True
        ordering = ['centrocusto']
        db_table = 'centro_custo'
