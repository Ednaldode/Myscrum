# Generated by Django 3.0.4 on 2020-03-26 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id_departamento', models.AutoField(primary_key=True, serialize=False)),
                ('departamento', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'departamento',
                'managed': True,
            },
        ),
    ]