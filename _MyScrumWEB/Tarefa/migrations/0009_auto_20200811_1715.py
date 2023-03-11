# Generated by Django 3.0.5 on 2020-08-11 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('_Login', '0003_listarpessoas'),
        ('Tarefa', '0008_auto_20200806_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportarTarefas',
            fields=[
                ('id_tarefa', models.AutoField(primary_key=True, serialize=False)),
                ('descri', models.TextField(blank=True, null=True)),
                ('prioridade', models.IntegerField(blank=True, null=True)),
                ('centro_custo', models.CharField(max_length=255)),
                ('stat', models.CharField(blank=True, max_length=20, null=True)),
                ('tamanho', models.CharField(max_length=255)),
                ('porcentagem', models.IntegerField(blank=True, null=True)),
                ('prazo', models.IntegerField(blank=True, null=True)),
                ('data_ini', models.DateField(blank=True, null=True)),
                ('data_real', models.DateField(blank=True, null=True)),
                ('data_fim', models.DateField(blank=True, null=True)),
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
                ('pendente_por', models.CharField(blank=True, max_length=45, null=True)),
                ('status_pendencia', models.TextField()),
                ('historico', models.TextField()),
                ('departamento', models.CharField(max_length=255)),
                ('responsavel', models.CharField(blank=True, max_length=45, null=True)),
                ('autoridade', models.CharField(blank=True, max_length=45, null=True)),
                ('etapa', models.CharField(max_length=255)),
                ('subetapa', models.CharField(max_length=255)),
                ('processo_relacionado', models.CharField(max_length=255)),
                ('predecessor1', models.IntegerField(blank=True, null=True)),
                ('predecessor2', models.IntegerField(blank=True, null=True)),
                ('predecessor3', models.IntegerField(blank=True, null=True)),
                ('checado', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'ExportarTarefas',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='tarefa',
            name='r5w2hT',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='executor',
            name='executor1',
            field=models.ForeignKey(db_column='executor1', default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor1', to='_Login.Pessoa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='executor',
            name='executor10',
            field=models.ForeignKey(blank=True, db_column='executor10', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor10', to='_Login.Pessoa'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='executor2',
            field=models.ForeignKey(blank=True, db_column='executor2', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor2', to='_Login.Pessoa'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='executor3',
            field=models.ForeignKey(blank=True, db_column='executor3', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor3', to='_Login.Pessoa'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='executor4',
            field=models.ForeignKey(blank=True, db_column='executor4', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor4', to='_Login.Pessoa'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='executor5',
            field=models.ForeignKey(blank=True, db_column='executor5', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor5', to='_Login.Pessoa'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='executor6',
            field=models.ForeignKey(blank=True, db_column='executor6', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor6', to='_Login.Pessoa'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='executor7',
            field=models.ForeignKey(blank=True, db_column='executor7', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor7', to='_Login.Pessoa'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='executor8',
            field=models.ForeignKey(blank=True, db_column='executor8', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor8', to='_Login.Pessoa'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='executor9',
            field=models.ForeignKey(blank=True, db_column='executor9', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='executor9', to='_Login.Pessoa'),
        ),
        migrations.AlterField(
            model_name='executor',
            name='porcento1',
            field=models.IntegerField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='autoridade',
            field=models.ForeignKey(db_column='autoridade', default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='autoridade', to='_Login.Pessoa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='checado',
            field=models.ForeignKey(db_column='checado', default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='checado', to='_Login.Pessoa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='pendente_por',
            field=models.ForeignKey(db_column='pendente_por', default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='pendente_por', to='_Login.Pessoa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tarefa',
            name='responsavel',
            field=models.ForeignKey(db_column='responsavel', default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='responsavel', to='_Login.Pessoa'),
            preserve_default=False,
        ),
    ]
