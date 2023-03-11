from django.db import models

# Create your models here.

class Processos(models.Model):
    id_processo = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    processo = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        ordering = ['processo']
        db_table = 'processos'
