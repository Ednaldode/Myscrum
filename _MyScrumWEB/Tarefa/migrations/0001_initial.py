# Generated by Django 3.0.4 on 2020-03-26 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Processo', '0001_initial'),
        ('Tamanho', '0001_initial'),
        ('Centro_de_custo', '0001_initial'),
        ('_Login', '0001_initial'),
        ('Departamento', '0001_initial'),
        ('Etapa', '0001_initial'),
        ('Sub_etapa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivos',
            fields=[
                ('idarquivos', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('arquivo', models.TextField()),
            ],
            options={
                'db_table': 'arquivos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tarefa',
            fields=[
                ('id_tarefa', models.AutoField(primary_key=True, serialize=False)),
                ('descri', models.TextField(blank=True, null=True)),
                ('prioridade', models.IntegerField(blank=True, null=True)),
                ('stat', models.CharField(blank=True, max_length=20, null=True)),
                ('porcentagem', models.IntegerField(blank=True, null=True)),
                ('prazo', models.IntegerField(blank=True, null=True)),
                ('data_ini', models.DateField(blank=True, null=True)),
                ('data_real', models.DateField(blank=True, null=True)),
                ('data_fim', models.DateField(blank=True, null=True)),
                ('pendente_por', models.CharField(blank=True, max_length=45, null=True)),
                ('status_pendencia', models.TextField(blank=True, null=True)),
                ('historico', models.TextField(blank=True, null=True)),
                ('responsavel', models.CharField(blank=True, max_length=45, null=True)),
                ('autoridade', models.CharField(blank=True, max_length=45, null=True)),
                ('dpto_correto', models.CharField(blank=True, max_length=45, null=True)),
                ('last_update', models.DateTimeField()),
                ('checado', models.CharField(blank=True, max_length=45, null=True)),
                ('anexo1', models.ForeignKey(blank=True, db_column='anexo1', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Anexo1', to='Tarefa.Arquivos')),
                ('anexo2', models.ForeignKey(blank=True, db_column='anexo2', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Anexo2', to='Tarefa.Arquivos')),
                ('anexo3', models.ForeignKey(blank=True, db_column='anexo3', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Anexo3', to='Tarefa.Arquivos')),
                ('anexo4', models.ForeignKey(blank=True, db_column='anexo4', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Anexo4', to='Tarefa.Arquivos')),
                ('etapa', models.ForeignKey(blank=True, db_column='etapa', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Etapa.Etapas')),
                ('id_centro_custo', models.ForeignKey(db_column='id_centro_custo', on_delete=django.db.models.deletion.DO_NOTHING, to='Centro_de_custo.CentroCusto')),
                ('id_departamento', models.ForeignKey(db_column='id_departamento', on_delete=django.db.models.deletion.DO_NOTHING, to='Departamento.Departamento')),
                ('id_pessoa', models.ForeignKey(db_column='id_pessoa', on_delete=django.db.models.deletion.DO_NOTHING, related_name='creator', to='_Login.Pessoa')),
                ('id_tamanho', models.ForeignKey(db_column='id_tamanho', on_delete=django.db.models.deletion.DO_NOTHING, to='Tamanho.Tamanho')),
                ('id_update', models.ForeignKey(db_column='id_update', on_delete=django.db.models.deletion.DO_NOTHING, related_name='updater', to='_Login.Pessoa')),
                ('predecessor_1', models.ForeignKey(blank=True, db_column='predecessor_1', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Predecessor_1', to='Tarefa.Tarefa')),
                ('predecessor_2', models.ForeignKey(blank=True, db_column='predecessor_2', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Predecessor_2', to='Tarefa.Tarefa')),
                ('predecessor_3', models.ForeignKey(blank=True, db_column='predecessor_3', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Predecessor_3', to='Tarefa.Tarefa')),
                ('processo_relacionado', models.ForeignKey(blank=True, db_column='processo_relacionado', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Processo.Processos')),
                ('subetapa', models.ForeignKey(blank=True, db_column='subetapa', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Sub_etapa.SubEtapas')),
            ],
            options={
                'db_table': 'tarefa',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Executor',
            fields=[
                ('id_executor', models.AutoField(primary_key=True, serialize=False)),
                ('executor1', models.CharField(blank=True, max_length=45, null=True)),
                ('porcento1', models.IntegerField(blank=True, null=True)),
                ('executor2', models.CharField(blank=True, max_length=45, null=True)),
                ('porcento2', models.IntegerField(blank=True, null=True)),
                ('executor3', models.CharField(blank=True, max_length=45, null=True)),
                ('porcento3', models.IntegerField(blank=True, null=True)),
                ('executor4', models.CharField(blank=True, max_length=45, null=True)),
                ('porcento4', models.IntegerField(blank=True, null=True)),
                ('executor5', models.CharField(blank=True, max_length=45, null=True)),
                ('porcento5', models.IntegerField(blank=True, null=True)),
                ('executor6', models.CharField(blank=True, max_length=45, null=True)),
                ('porcento6', models.IntegerField(blank=True, null=True)),
                ('executor7', models.CharField(blank=True, max_length=45, null=True)),
                ('porcento7', models.IntegerField(blank=True, null=True)),
                ('executor8', models.CharField(blank=True, max_length=45, null=True)),
                ('porcento8', models.IntegerField(blank=True, null=True)),
                ('executor9', models.CharField(blank=True, max_length=45, null=True)),
                ('porcento9', models.IntegerField(blank=True, null=True)),
                ('executor10', models.CharField(blank=True, max_length=45, null=True)),
                ('porcento10', models.IntegerField(blank=True, null=True)),
                ('id_tarefa', models.ForeignKey(db_column='id_tarefa', on_delete=django.db.models.deletion.DO_NOTHING, to='Tarefa.Tarefa')),
            ],
            options={
                'db_table': 'executor',
                'managed': True,
            },
        ),
    ]