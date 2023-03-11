# Generated by Django 2.2 on 2020-08-18 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TarefasHome',
            fields=[
                ('id_tarefa', models.AutoField(primary_key=True, serialize=False)),
                ('stat', models.CharField(blank=True, max_length=20, null=True)),
                ('porcentagem', models.IntegerField(blank=True, null=True)),
                ('tamanho', models.CharField(max_length=6)),
                ('prazo', models.IntegerField(blank=True, null=True)),
                ('data_ini', models.DateField(blank=True, null=True)),
                ('data_real', models.DateField(blank=True, null=True)),
                ('data_fim', models.DateField(blank=True, null=True)),
                ('pendente_por', models.CharField(blank=True, max_length=45, null=True)),
                ('responsavel', models.CharField(blank=True, max_length=45, null=True)),
                ('autoridade', models.CharField(blank=True, max_length=45, null=True)),
                ('checado', models.CharField(blank=True, max_length=45, null=True)),
                ('processo_relacionado', models.CharField(max_length=255)),
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
            ],
            options={
                'db_table': 'TarefasHome',
                'managed': False,
            },
        ),
    ]
