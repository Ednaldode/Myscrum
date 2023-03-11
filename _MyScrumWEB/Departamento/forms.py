# Imports do Django
from django import forms

# Imports do mesmo App
from .models import Departamento

# Import Biblioteca Python


class DepartamentoForms(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['departamento']