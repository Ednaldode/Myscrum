from django.db import models

# Create your models here.

class Tamanho(models.Model):
    id_tamanho = models.AutoField(primary_key=True)
    peso = models.FloatField(blank=True, null=True)
    descricao = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tamanho'