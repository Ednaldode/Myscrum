# Generated by Django 2.2 on 2020-07-09 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tarefa', '0004_auto_20200709_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retrospectiva',
            name='finalizado',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
