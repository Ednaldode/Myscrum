# Generated by Django 2.2 on 2020-08-18 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Processo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='processos',
            options={'managed': True, 'ordering': ['processo']},
        ),
    ]
