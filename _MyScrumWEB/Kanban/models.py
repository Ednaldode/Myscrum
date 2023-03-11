from django.db import models

# Create your models here.

class TarefasKanban(models.Model):
    id_tarefa = models.AutoField(primary_key=True)
    descri = models.TextField(blank=True, null=True)
    prioridade = models.IntegerField(blank=True, null=True)
    stat = models.CharField(max_length=20, blank=True, null=True)
    porcentagem = models.IntegerField(blank=True, null=True)
    tamanho = models.CharField(max_length=6)
    prazo = models.IntegerField(blank=True, null=True)
    data_ini = models.DateField(blank=True, null=True)
    data_real = models.DateField(blank=True, null=True)
    data_fim = models.DateField(blank=True, null=True)
    pendente_por = models.CharField(max_length=45, blank=True, null=True)
    responsavel = models.CharField(max_length=45, blank=True, null=True)
    autoridade = models.CharField(max_length=45, blank=True, null=True)
    checado = models.CharField(max_length=45, blank=True, null=True)
    status_pendencia = models.TextField(blank=True, null=True)
    historico = models.TextField(blank=True, null=True)
    departamento = models.CharField(max_length=255)
    centro_custo = models.CharField(max_length=255)
    etapa = models.CharField(max_length=255)
    subetapa = models.CharField(max_length=255)
    anexo1 = models.TextField(blank=True, null=True)
    anexo2 = models.TextField(blank=True, null=True)
    anexo3 = models.TextField(blank=True, null=True)
    anexo4 = models.TextField(blank=True, null=True)
    predecessor_1 = models.TextField(blank=True, null=True)
    predecessor_2 = models.TextField(blank=True, null=True)
    predecessor_3 = models.TextField(blank=True, null=True)
    processo_relacionado = models.CharField(max_length=255)
    Executores = models.CharField(max_length=45, blank=True, null=True)
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
    retrospec = models.CharField(max_length=255, blank=True, null=True)
    r5w2hT = models.IntegerField(blank=True, null=True)
    last_update = models.DateTimeField()
    atualizado_por = models.CharField(max_length=255)
    criado_por = models.CharField(max_length=255)
    id_filho = models.IntegerField(blank=True, null=True)
    id_juridico = models.IntegerField(blank=True, null=True)
    id_locacao = models.IntegerField(blank=True, null=True)
    id_status = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'TarefasKanban'