# Generated by Django 2.2 on 2020-08-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tarefa', '0009_auto_20200811_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exportartarefas',
            old_name='predecessor1',
            new_name='predecessor_1',
        ),
        migrations.RenameField(
            model_name='exportartarefas',
            old_name='predecessor2',
            new_name='predecessor_2',
        ),
        migrations.RenameField(
            model_name='exportartarefas',
            old_name='predecessor3',
            new_name='predecessor_3',
        ),
        migrations.AddField(
            model_name='exportartarefas',
            name='r5w2hT',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='retrospectiva',
            name='finalizado',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]