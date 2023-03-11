from django.db import models
from Departamento.models import Departamento
from Centro_de_custo.models import CentroCusto

# Create your models here.

class Pessoa(models.Model):
    id_pessoa = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    id_advocacia = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    senha = models.CharField(max_length=45, blank=True, null=True)
    login = models.CharField(max_length=20, blank=True, null=True)
    ativo = models.IntegerField(blank=True, null=True)
    adm = models.IntegerField(blank=True, null=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento')
    observacao = models.TextField(blank=True, null=True)
    salario = models.FloatField(blank=True, null=True)
    carga_horaria = models.IntegerField(blank=True, null=True)
    id_centrocusto = models.ForeignKey(CentroCusto, models.DO_NOTHING, db_column='id_centrocusto')
    id_user = models.OneToOneField('auth.User', on_delete=models.PROTECT, null=True)
    data_contratacao = models.DateField(blank=True)

    class Meta:
        managed = True
        ordering = ['nome']
        db_table = 'pessoa'

class Vinculos(models.Model):
    id_vinculos = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='id_usuario')
    id_empresa = models.IntegerField(blank=True, null=True)
    id_cc = models.ForeignKey(CentroCusto, models.DO_NOTHING, db_column='id_cc', blank=True, null=True)
    id_dpto = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_dpto', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'vinculos'

class ListarPessoas(models.Model):
    id_pessoa = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    nome = models.CharField(max_length=45, blank=True, null=True)
    login = models.CharField(max_length=20, blank=True, null=True)
    ativo = models.IntegerField(blank=True, null=True)
    adm = models.IntegerField(blank=True, null=True)
    departamento = models.CharField(max_length=255)
    centro_custo = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ListarPessoas'