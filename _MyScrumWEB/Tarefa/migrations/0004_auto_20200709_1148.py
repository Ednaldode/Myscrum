# Generated by Django 2.2 on 2020-07-09 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tarefa', '0003_tarefa_retrospectiva'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarefa',
            old_name='retrospectiva',
            new_name='retrospec',
        ),
        migrations.CreateModel(
            name='Retrospectiva',
            fields=[
                ('id_retrospectiva', models.AutoField(primary_key=True, serialize=False)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('stats', models.CharField(blank=True, max_length=20, null=True)),
                ('finalizado', models.BooleanField()),
                ('id_tarefa', models.ForeignKey(db_column='id_tarefa', on_delete=django.db.models.deletion.DO_NOTHING, to='Tarefa.Tarefa')),
            ],
            options={
                'db_table': 'retrospectiva',
                'managed': True,
            },
        ),
    ]
