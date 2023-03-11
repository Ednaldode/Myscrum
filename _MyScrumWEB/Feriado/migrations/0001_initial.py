# Generated by Django 2.2 on 2020-08-18 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feriados',
            fields=[
                ('id_feriado', models.AutoField(primary_key=True, serialize=False)),
                ('data_feriado', models.DateField(blank=True, null=True)),
                ('descri_feriado', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'feriados',
                'managed': True,
            },
        ),
    ]
