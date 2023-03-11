# Imports do Django
from django import forms
from django.contrib.auth.models import User

# Imports do mesmo App
from .models import Pessoa

# Imports de outros Apps
from Centro_de_custo.models import CentroCusto
from Departamento.models import Departamento

# Import Biblioteca Python


class PessoaForms(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PessoaForms, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        self.fields['id_departamento'].queryset = Departamento.objects.all()
        self.fields['id_departamento'].label_from_instance = lambda obj:(obj.departamento)

        self.fields['id_centrocusto'].queryset = CentroCusto.objects.all()
        self.fields['id_centrocusto'].label_from_instance = lambda obj:(obj.centrocusto)

    class Meta:
        model = Pessoa
        fields = ['nome', 'email', 'id_departamento', 'id_centrocusto', 'observacao', 'salario',
        'carga_horaria', 'ativo', 'adm', 'data_contratacao',
        ]

class profileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']