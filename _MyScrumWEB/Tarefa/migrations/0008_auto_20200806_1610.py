# Generated by Django 2.2 on 2020-08-06 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('_Login', '0002_auto_20200422_1556'),
        ('Tarefa', '0007_auto_20200805_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retrospectiva',
            name='id_update',
            field=models.ForeignKey(db_column='id_update', on_delete=django.db.models.deletion.DO_NOTHING, to='_Login.Pessoa'),
        ),
        migrations.CreateModel(
            name='R5w2h',
            fields=[
                ('id_5w2h', models.AutoField(primary_key=True, serialize=False)),
                ('rWhat', models.TextField(blank=True, null=True)),
                ('rWhy', models.TextField(blank=True, null=True)),
                ('rWhere', models.TextField(blank=True, null=True)),
                ('rWhen', models.TextField(blank=True, null=True)),
                ('rWho', models.TextField(blank=True, null=True)),
                ('rHow', models.TextField(blank=True, null=True)),
                ('rHowMuch', models.TextField(blank=True, null=True)),
                ('last_update', models.DateTimeField()),
                ('id_tarefa', models.ForeignKey(db_column='id_tarefa', on_delete=django.db.models.deletion.DO_NOTHING, to='Tarefa.Tarefa')),
                ('id_update', models.ForeignKey(db_column='id_update', on_delete=django.db.models.deletion.DO_NOTHING, to='_Login.Pessoa')),
            ],
            options={
                'db_table': 'r5w2h',
                'managed': True,
            },
        ),
    ]
