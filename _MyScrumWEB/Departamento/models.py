from django.db import models

# Create your models here.

class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    id_empresa = models.IntegerField(blank=True, null=True)
    imagem = models.FileField(upload_to='')
    departamento = models.CharField(max_length=45)

    class Meta:
        managed = True
        ordering = ['departamento']
        db_table = 'departamento'
