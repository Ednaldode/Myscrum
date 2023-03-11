from django.db import models
from Centro_de_custo.models import CentroCusto
from Tamanho.models import Tamanho
from Departamento.models import Departamento
from Processo.models import Processos
from _Login.models import Pessoa
from Etapa.models import Etapas
from Sub_etapa.models import SubEtapas

# Create your models here.
class Arquivos(models.Model):
    idarquivos = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    arquivo = models.TextField()

    class Meta:
        managed = True
        db_table = 'arquivos'

class Tarefa(models.Model):
    id_tarefa = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    descri = models.TextField(blank=True, null=True)
    id_centro_custo = models.ForeignKey(CentroCusto, models.DO_NOTHING, db_column='id_centro_custo')
    prioridade = models.IntegerField(blank=True, null=True)
    stat = models.CharField(max_length=20, blank=True, null=True)
    id_tamanho = models.ForeignKey(Tamanho, models.DO_NOTHING, db_column='id_tamanho')
    porcentagem = models.IntegerField(blank=True, null=True)
    prazo = models.IntegerField(blank=True, null=True)
    data_ini = models.DateField(blank=True, null=True)
    data_real = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    data_finalizacao = models.DateField(blank=True, null=True)
    data_finalizacao_sat = models.DateField(blank=True, null=True)
    pendente_por = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='pendente_por', related_name='pendente_por', blank=True, null=True)
    status_pendencia = models.TextField(blank=True, null=True)
    historico = models.TextField(blank=True, null=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento')
    responsavel = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='responsavel', related_name='responsavel')
    autoridade = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='autoridade', related_name='autoridade')
    dpto_correto = models.CharField(max_length=45, blank=True, null=True)
    processo_relacionado = models.ForeignKey(Processos, models.DO_NOTHING, db_column='processo_relacionado', blank=True, null=True)
    id_pessoa = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='id_pessoa', related_name='creator')
    last_update = models.DateTimeField(auto_now=True)
    id_update = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='id_update', related_name='updater')
    predecessor_1 = models.ForeignKey('self', models.DO_NOTHING, db_column='predecessor_1', blank=True, null=True, related_name='Predecessor_1')
    predecessor_2 = models.ForeignKey('self', models.DO_NOTHING, db_column='predecessor_2', blank=True, null=True, related_name='Predecessor_2')
    predecessor_3 = models.ForeignKey('self', models.DO_NOTHING, db_column='predecessor_3', blank=True, null=True, related_name='Predecessor_3')
    anexo1 = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='anexo1', blank=True, null=True, related_name='Anexo1')
    anexo2 = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='anexo2', blank=True, null=True, related_name='Anexo2')
    anexo3 = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='anexo3', blank=True, null=True, related_name='Anexo3')
    anexo4 = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='anexo4', blank=True, null=True, related_name='Anexo4')
    checado = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='checado', related_name='checado')
    etapa = models.ForeignKey(Etapas, models.DO_NOTHING, db_column='etapa', blank=True, null=True)
    subetapa = models.ForeignKey(SubEtapas, models.DO_NOTHING, db_column='subetapa', blank=True, null=True)
    r5w2hT = models.IntegerField(blank=True, null=True)
    retrospec = models.CharField(max_length=20, blank=True, null=True)
    calendario = models.IntegerField(blank=True, null=True)
    data_calendario = models.DateTimeField(blank=True, null=True)
    id_filho = models.IntegerField(blank=True, null=True)
    id_locacao = models.IntegerField(blank=True, null=True)
    id_juridico = models.IntegerField(blank=True, null=True)
    id_status = models.IntegerField(blank=True, null=True)
    id_medicao = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tarefa'

class Executor(models.Model):
    id_executor = models.AutoField(primary_key=True)
    executor1 = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='executor1', related_name='executor1')
    porcento1 = models.IntegerField(blank=True)
    executor2 = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='executor2', related_name='executor2',blank=True, null=True)
    porcento2 = models.IntegerField(blank=True, null=True)
    executor3 = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='executor3', related_name='executor3',blank=True, null=True)
    porcento3 = models.IntegerField(blank=True, null=True)
    executor4 = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='executor4', related_name='executor4',blank=True, null=True)
    porcento4 = models.IntegerField(blank=True, null=True)
    executor5 = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='executor5', related_name='executor5',blank=True, null=True)
    porcento5 = models.IntegerField(blank=True, null=True)
    executor6 = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='executor6', related_name='executor6',blank=True, null=True)
    porcento6 = models.IntegerField(blank=True, null=True)
    executor7 = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='executor7', related_name='executor7',blank=True, null=True)
    porcento7 = models.IntegerField(blank=True, null=True)
    executor8 = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='executor8', related_name='executor8',blank=True, null=True)
    porcento8 = models.IntegerField(blank=True, null=True)
    executor9 = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='executor9', related_name='executor9',blank=True, null=True)
    porcento9 = models.IntegerField(blank=True, null=True)
    executor10 = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='executor10', related_name='executor10',blank=True, null=True)
    porcento10 = models.IntegerField(blank=True, null=True)
    id_tarefa = models.ForeignKey('Tarefa', models.DO_NOTHING, db_column='id_tarefa')

    class Meta:
        managed = True
        db_table = 'executor'

class ListarTarefas(models.Model):
    id_tarefa = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    descri = models.TextField(blank=True, null=True)
    centro_custo = models.CharField(max_length=255)
    etapa = models.CharField(max_length=255)
    subetapa = models.CharField(max_length=255)
    prioridade = models.IntegerField(blank=True, null=True)
    stat = models.CharField(max_length=20, blank=True, null=True)
    porcentagem = models.IntegerField(blank=True, null=True)
    data_ini = models.DateField(blank=True, null=True)
    data_real = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    pendente_por = models.CharField(max_length=45, blank=True, null=True)
    departamento = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=45, blank=True, null=True)
    autoridade = models.CharField(max_length=45, blank=True, null=True)
    checado = models.CharField(max_length=45, blank=True, null=True)
    processo_relacionado = models.CharField(max_length=255)
    executor1 = models.CharField(max_length=45, blank=True, null=True)
    porcento1 = models.IntegerField(blank=True, null=True)
    executor2 = models.CharField(max_length=45, blank=True, null=True)
    porcento2 = models.IntegerField(blank=True, null=True)
    executor3 = models.CharField(max_length=45, blank=True, null=True)
    porcento3 = models.IntegerField(blank=True, null=True)
    executor4 = models.CharField(max_length=45, blank=True, null=True)
    porcento4 = models.IntegerField(blank=True, null=True)
    executor5 = models.CharField(max_length=45, blank=True, null=True)
    porcento5 = models.IntegerField(blank=True, null=True)
    executor6 = models.CharField(max_length=45, blank=True, null=True)
    porcento6 = models.IntegerField(blank=True, null=True)
    executor7 = models.CharField(max_length=45, blank=True, null=True)
    porcento7 = models.IntegerField(blank=True, null=True)
    executor8 = models.CharField(max_length=45, blank=True, null=True)
    porcento8 = models.IntegerField(blank=True, null=True)
    executor9 = models.CharField(max_length=45, blank=True, null=True)
    porcento9 = models.IntegerField(blank=True, null=True)
    executor10 = models.CharField(max_length=45, blank=True, null=True)
    porcento10 = models.IntegerField(blank=True, null=True)
    r5w2hT = models.IntegerField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'ListarTarefas'

    def __str__(self):
        return self.id_tarefa

class R5w2h(models.Model):
    id_5w2h = models.AutoField(primary_key=True)
    id_tarefa = models.ForeignKey(Tarefa, models.DO_NOTHING, db_column='id_tarefa')
    rWhat = models.TextField(blank=True, null=True)
    rWhy = models.TextField(blank=True, null=True)
    rWhere = models.TextField(blank=True, null=True)
    rWhen = models.TextField(blank=True, null=True)
    rWho = models.TextField(blank=True, null=True)
    rHow = models.TextField(blank=True, null=True)
    rHowMuch = models.TextField(blank=True, null=True)
    id_update = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='id_update')
    last_update = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'r5w2h'

class Retrospectiva(models.Model):
    id_retrospectiva = models.AutoField(primary_key=True)
    id_tarefa = models.ForeignKey(Tarefa, models.DO_NOTHING, db_column='id_tarefa')
    descricao = models.TextField(blank=True, null=True)
    r_historico = models.TextField(blank=True, null=True)
    stats = models.CharField(max_length=20, blank=True, null=True)
    finalizado = models.BooleanField(blank=True, default=False)
    id_update = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='id_update', related_name='id_update')
    id_responsavel = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='id_responsavel', related_name='id_responsavel')
    nome_responsavel = models.CharField(max_length=45, blank=True, null=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'retrospectiva'

class ExportarTarefas(models.Model):
    id_tarefa = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    descri = models.TextField(blank=True, null=True)
    prioridade = models.IntegerField(blank=True, null=True)
    centro_custo = models.CharField(max_length=255)
    stat = models.CharField(max_length=20, blank=True, null=True)
    tamanho = models.CharField(max_length=255)
    porcentagem = models.IntegerField(blank=True, null=True)
    prazo = models.IntegerField(blank=True, null=True)
    data_ini = models.DateField(blank=True, null=True)
    data_real = models.DateField(blank=True, null=True)
    data_finalizacao = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    executor1 = models.CharField(max_length=45, blank=True, null=True)
    porcento1 = models.IntegerField(blank=True, null=True)
    executor2 = models.CharField(max_length=45, blank=True, null=True)
    porcento2 = models.IntegerField(blank=True, null=True)
    executor3 = models.CharField(max_length=45, blank=True, null=True)
    porcento3 = models.IntegerField(blank=True, null=True)
    executor4 = models.CharField(max_length=45, blank=True, null=True)
    porcento4 = models.IntegerField(blank=True, null=True)
    executor5 = models.CharField(max_length=45, blank=True, null=True)
    porcento5 = models.IntegerField(blank=True, null=True)
    executor6 = models.CharField(max_length=45, blank=True, null=True)
    porcento6 = models.IntegerField(blank=True, null=True)
    executor7 = models.CharField(max_length=45, blank=True, null=True)
    porcento7 = models.IntegerField(blank=True, null=True)
    executor8 = models.CharField(max_length=45, blank=True, null=True)
    porcento8 = models.IntegerField(blank=True, null=True)
    executor9 = models.CharField(max_length=45, blank=True, null=True)
    porcento9 = models.IntegerField(blank=True, null=True)
    executor10 = models.CharField(max_length=45, blank=True, null=True)
    porcento10 = models.IntegerField(blank=True, null=True)
    pendente_por = models.CharField(max_length=45, blank=True, null=True)
    status_pendencia = models.TextField()
    historico = models.TextField()
    departamento = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=45, blank=True, null=True)
    autoridade = models.CharField(max_length=45, blank=True, null=True)
    etapa = models.CharField(max_length=255)
    subetapa = models.CharField(max_length=255)
    processo_relacionado = models.CharField(max_length=255)
    predecessor_1 = models.IntegerField(blank=True, null=True)
    predecessor_2 = models.IntegerField(blank=True, null=True)
    predecessor_3 = models.IntegerField(blank=True, null=True)
    checado = models.CharField(max_length=45, blank=True, null=True)
    r5w2hT = models.IntegerField(blank=True, null=True)
    id_filho = models.IntegerField(blank=True, null=True)
    id_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ExportarTarefas'
