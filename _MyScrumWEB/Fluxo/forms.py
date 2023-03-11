# Imports do Django
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext as _

# Imports do mesmo App
from .models import LocacaoEditar, MedicaoTerceiros

# Imports de outros Apps
from _Login.models import Pessoa
from Tarefa.models import Tarefa, Executor
from Departamento.models import Departamento
from Tamanho.models import Tamanho

# Import Biblioteca Python
import datetime

class EditarLocacao(forms.ModelForm):
    PRAZO_CHOICES = (
    (0, _("0")),
    (1, _("1")),
    (2, _("2")),
    (3, _("3")),
    (5, _("5")),
    (8, _("8")),
    (13, _("13")),
    (21, _("21")),
    (34, _("34")),
    (55, _("55")),
    (89, _("89")),
    (144, _("144")),
    (233, _("233")),
    (377, _("377")),
    (610, _("610")),
    (987, _("987")),
    )

    id_editar_locacao = forms.IntegerField(required=False)
    descricao = forms.CharField(label='Descrição', max_length=300, required=False, widget=forms.Textarea)
    prazo = forms.ChoiceField(choices=PRAZO_CHOICES, required=False)
    id_tamanho = forms.ModelChoiceField(queryset=Tamanho.objects.all())
    status_pendencia = forms.CharField(label='Status Pendência', max_length=300, required=False)

    id_departamento = forms.ModelChoiceField(queryset=Departamento.objects.all())
    id_responsavel = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1))
    id_autoridade = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1))
    id_checado = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    id_pendente_por = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1),required=False)
    
    id_executor1 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    porcento1 = forms.IntegerField(required=False)
    id_executor2 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    porcento2 = forms.IntegerField(required=False)
    id_executor3 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    porcento3 = forms.IntegerField(required=False)
    id_executor4 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    porcento4 = forms.IntegerField(required=False)
    id_executor5 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    porcento5 = forms.IntegerField(required=False)
    id_executor6 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    porcento6 = forms.IntegerField(required=False)
    id_executor7 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    porcento7 = forms.IntegerField(required=False)
    id_executor8 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    porcento8 = forms.IntegerField(required=False)
    id_executor9 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    porcento9 = forms.IntegerField(required=False)
    id_executor10 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    porcento10 = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(EditarLocacao, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        self.fields['id_tamanho'].queryset = Tamanho.objects.all()
        self.fields['id_tamanho'].label_from_instance = lambda obj:(obj.descricao)

        self.fields['id_departamento'].queryset = Departamento.objects.all()
        self.fields['id_departamento'].label_from_instance = lambda obj:(obj.departamento)

        self.fields['id_responsavel'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_responsavel'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_autoridade'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_autoridade'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_checado'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_checado'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_pendente_por'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_pendente_por'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_pessoa'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_pessoa'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_update'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_update'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_executor1'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_executor1'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_executor2'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_executor2'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_executor3'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_executor3'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_executor4'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_executor4'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_executor5'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_executor5'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_executor6'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_executor6'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_executor7'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_executor7'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_executor8'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_executor8'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_executor9'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_executor9'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_executor10'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['id_executor10'].label_from_instance = lambda obj:(obj.nome)

    class Meta:
        model = LocacaoEditar
        fields = '__all__'

class EditarMedicaoTerceiros(forms.ModelForm):
    MES_CHOICES = (
    (0, _("---------")),
    (1, _("Janeiro")),
    (2, _("Fevereiro")),
    (3, _("Março")),
    (4, _("Abril")),
    (5, _("Maio")),
    (6, _("Junho")),
    (7, _("Julho")),
    (8, _("Agosto")),
    (9, _("Setembro")),
    (10, _("Outubro")),
    (11, _("Novembro")),
    (12, _("Dezembro")),
    )

    PERMUTA_CHOICES = (
    (0, _("Não")),
    (1, _("Sim")),
    )

    id_medicao_terceiros = forms.IntegerField(required=False)
    id_tarefa = forms.IntegerField(required=False)
    mes = forms.ChoiceField(choices=MES_CHOICES, required=False)
    valor_bruto = forms.CharField(label='Valor Bruto', max_length=50, required=False)
    valor_liquido = forms.CharField(label='Valor Liquido', max_length=50, required=False)
    permuta = forms.ChoiceField(choices=PERMUTA_CHOICES, required=False)

    class Meta:
        model = MedicaoTerceiros
        fields = '__all__'