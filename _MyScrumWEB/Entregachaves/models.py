from django.db import models


# Create your models here.
class Entrega(models.Model):
    id_entrega = models.AutoField(primary_key=True)
    empreendimento = models.TextField(blank=True, null=True)
    bloco = models.TextField(blank=True, null=True)
    apto = models.IntegerField(blank=True, null=True)
    data_entrega = models.DateField(blank=True, null=True, auto_now = True)
    data_assin = models.DateField(blank=True, null=True, auto_now = True)
    proprietario1 = models.TextField(blank=True, null=True)
    proprietario2 = models.TextField(blank=True, null=True)
    testemunha1 = models.TextField(blank=True, null=True)
    testemunha2 = models.TextField(blank=True, null=True)
    rg_proprietario1 = models.TextField(blank=True, null=True)
    rg_proprietario2 = models.TextField(blank=True, null=True)
    rg_testemunha1 = models.TextField(blank=True, null=True)
    rg_testemunha2 = models.TextField(blank=True, null=True)
    cpf_proprietario1 = models.TextField(blank=True, null=True)
    cpf_proprietario2 = models.TextField(blank=True, null=True)
    cpf_testemunha1 = models.TextField(blank=True, null=True)
    cpf_testemunha2 = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'entrega_chaves'
