# Imports do Django
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext as _

#
from .models import Solicitacao, Problema
from _Login.models import Pessoa
from Tarefa.models import Tarefa, Executor

# Import Biblioteca Python
import datetime

class ListarForms(forms.ModelForm):

    class Meta:
        model = Tarefa
        fields = '__all__'

class ImpressaoForms(forms.ModelForm):    
    class Meta:
        model = Tarefa
        fields = '__all__'

class DashboardsForms(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = '__all__'

class SolicitacaoForms(forms.ModelForm):

    STATUS_CHOICES = (
    ('A fazer', _("A fazer")),
    ('Fazendo', _("Fazendo")),
    ('Feito', _("Feito")),
    ('Cancelado', _("Cancelado"))
    )

    PROCESSO_CHOICES = (
    ('---', _("---")),
    ('Análise', _("Análise")),
    ('Agendamento', _("Agendamento")),
    ('Atendimento', _("Atendimento")),
    ('Termo de Quitação', _("Termo de Quitação")),
    ('Concluído', _("Concluído")),
    ('Fora de Garantia', _("Fora de Garantia"))
    )

    EMPREENDIMENTO_CHOICES = (
    ('---', _("---")),
    ('Le Jardin', _("Le Jardin")),
    ('Villa Helvétia', _("Villa Helvétia")),
    ('Vista Verde', _("Vista Verde")),
    ('Grand Ville', _("Grand Ville")),
    ('Belvedere', _("Belvedere")),
    ('Duetto D Mariah', _("Duetto D Mariah")),
    ('Grand Ville Residencial', _("Grand Ville Residencial")),
    ('Imagine', _("Imagine")),
    ('Loft Ekko House', _("Loft Ekko House")),
    ('Montis Residence', _("Montis Residence")),
    ('Parque Árvores', _("Parque Árvores")),
    ('Parque Flores', _("Parque Flores")),
    ('Parque Pássaros', _("Parque Pássaros")),
    ('Villagio D Amore', _("Villagio D Amore")),
    ('Terceiro', _("Terceiro")),
    )

    BLOCO_LEJARDIN = (
    ('TESTE', _("TESTE")),
    )

    BLOCOS_CHOICES = (
    ('---', _("---")),
    ('A', _("A")),
    ('B', _("B")),
    ('C', _("C")),
    ('D', _("D")),
    ('E', _("E")),
    ('F', _("F")),
    ('G', _("G")),
    ('H', _("H")),
    ('I', _("I")),
    ('J', _("J")),
    ('K', _("K")),
    ('II', _("II")),
    ('III', _("III")),
    ('IV', _("IV")),
    ('V', _("V")),
    ('VI', _("VI")),
    ('VII', _("VII")),
    ('CANNES', _("CANNES")),
    ('LYON', _("LYON")),
    ('BOURDEAUX', _("BOURDEAUX")),
    )

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

    REPARO_CHOICES = (
    ('---', _("---")),
    ('Elétrica', _("Elétrica")),
    ('Hidráulica', _("Hidráulica")),
    ('Pintura', _("Pintura")),
    ('Pedreiro', _("Pedreiro")),
    ('Esquadrias', _("Esquadrias")),
    ('Gás', _("Gás")),
    ('Telefonia', _("Telefonia")),
    ('Limpeza', _("Limpeza")),
    ('Jardinagem ', _("Jardinagem "))
    )

    SOLICITACAO_CHOICES = (
    ('---', _("---")),
    ('Vistoria de Entrega', _("Vistoria de Entrega")),
    ('Garantia', _("Garantia")),
    )

    AMBIENTE_CHOICES = (
    ('---', _("---")),
    ('Sala', _("Sala")),
    ('Cozinha', _("Cozinha")),
    ('Quarto 1', _("Quarto 1")),
    ('Quarto 2', _("Quarto 2")),
    ('Banheiro 1', _("Banheiro 1")),
    ('Banheiro 2', _("Banheiro 2")),
    )

    PROCEDENCIA_CHOICES = (
    ('---', _("---")),
    ('Sim', _("Sim")),
    ('Sim com ressalva', _("Sim com ressalva")),
    ('Não', _("Não")),
    )

    TESTE_CHOICES = (
    ('---', _("---")),
    )

    #forms com as informações da manutenção
    responsavel = forms.CharField()
    autoridade = forms.CharField()
    porcentagem = forms.IntegerField()
    statusProcesso = forms.ChoiceField(choices=PROCESSO_CHOICES)
    processoRelacionado = forms.ChoiceField(choices=TESTE_CHOICES)
    dataIni = forms.DateField()
    empre_manut = forms.CharField()
    bloco_manut = forms.CharField()
    unidade_manut = forms.CharField()
    solicitante_manut_navbar = forms.CharField()
    solicitante_manut = forms.CharField()
    cpf_solicitante_manut = forms.CharField()
    rg_solicitante_manut = forms.CharField()
    email_solicitante_manut = forms.CharField()
    pessoa_contato_manut = forms.CharField()
    cpf_contato_manut = forms.CharField()
    rg_contato_manut = forms.CharField()
    email_contato_manut = forms.CharField()

    tempoTotal = forms.CharField()
    executorGeral1 = forms.CharField()
    executorGeral2 = forms.CharField()
    executorGeral3 = forms.CharField()
    tamanhoGeral = forms.CharField()
    tarefas = forms.CharField()

    #forms com as informações da solicitação
    stat = forms.ChoiceField(choices=STATUS_CHOICES)
    empreendimento = forms.ChoiceField(choices=EMPREENDIMENTO_CHOICES)
    bloco = forms.ChoiceField(choices=BLOCOS_CHOICES)

    solicitante = forms.CharField()
    cpf_solicitante = forms.IntegerField()
    rg_solicitante = forms.IntegerField()
    email_solicitante = forms.CharField()

    pessoaContato = forms.CharField()
    cpf_contato = forms.IntegerField()
    rg_contato = forms.IntegerField()
    email_contato = forms.CharField()

    ambiente = forms.ChoiceField(choices=AMBIENTE_CHOICES)
    ambiente2 = forms.ChoiceField(choices=AMBIENTE_CHOICES)
    ambiente3 = forms.ChoiceField(choices=AMBIENTE_CHOICES)
    ambiente4 = forms.ChoiceField(choices=AMBIENTE_CHOICES)
    ambiente5 = forms.ChoiceField(choices=AMBIENTE_CHOICES)
    ambiente6 = forms.ChoiceField(choices=AMBIENTE_CHOICES)
    ambiente7 = forms.ChoiceField(choices=AMBIENTE_CHOICES)
    ambiente8 = forms.ChoiceField(choices=AMBIENTE_CHOICES)
    ambiente9 = forms.ChoiceField(choices=AMBIENTE_CHOICES)
    ambiente10 = forms.ChoiceField(choices=AMBIENTE_CHOICES)

    descricao = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao2 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao3 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao4 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao5 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao6 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao7 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao8 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao9 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao10 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)

    descricao_problema = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao_problema2 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao_problema3 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao_problema4 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao_problema5 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao_problema6 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao_problema7 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao_problema8 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao_problema9 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    descricao_problema10 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)

    tipo_reparo= forms.ChoiceField(choices=REPARO_CHOICES)
    tipo_reparo2= forms.ChoiceField(choices=REPARO_CHOICES)
    tipo_reparo3= forms.ChoiceField(choices=REPARO_CHOICES)
    tipo_reparo4= forms.ChoiceField(choices=REPARO_CHOICES)
    tipo_reparo5= forms.ChoiceField(choices=REPARO_CHOICES)
    tipo_reparo6= forms.ChoiceField(choices=REPARO_CHOICES)
    tipo_reparo7= forms.ChoiceField(choices=REPARO_CHOICES)
    tipo_reparo8= forms.ChoiceField(choices=REPARO_CHOICES)
    tipo_reparo9= forms.ChoiceField(choices=REPARO_CHOICES)
    tipo_reparo10= forms.ChoiceField(choices=REPARO_CHOICES)

    procedencia = forms.ChoiceField(choices=PROCEDENCIA_CHOICES)
    procedencia2 = forms.ChoiceField(choices=PROCEDENCIA_CHOICES)
    procedencia3 = forms.ChoiceField(choices=PROCEDENCIA_CHOICES)
    procedencia4 = forms.ChoiceField(choices=PROCEDENCIA_CHOICES)
    procedencia5 = forms.ChoiceField(choices=PROCEDENCIA_CHOICES)
    procedencia6 = forms.ChoiceField(choices=PROCEDENCIA_CHOICES)
    procedencia7 = forms.ChoiceField(choices=PROCEDENCIA_CHOICES)
    procedencia8 = forms.ChoiceField(choices=PROCEDENCIA_CHOICES)
    procedencia9 = forms.ChoiceField(choices=PROCEDENCIA_CHOICES)
    procedencia10 = forms.ChoiceField(choices=PROCEDENCIA_CHOICES)

    historico = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    historico2 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    historico3 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    historico4 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    historico5 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    historico6 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    historico7 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    historico8 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    historico9 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    historico10 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)

    custo = forms.CharField()
    custo2 = forms.CharField()
    custo = forms.CharField()
    custo3 = forms.CharField()
    custo4 = forms.CharField()
    custo5 = forms.CharField()
    custo6 = forms.CharField()
    custo7 = forms.CharField()
    custo8 = forms.CharField()
    custo9 = forms.CharField()
    custo10 = forms.CharField()

    duracao = forms.CharField()
    duracao2 = forms.CharField()
    duracao3 = forms.CharField()
    duracao4 = forms.CharField()
    duracao5 = forms.CharField()
    duracao6 = forms.CharField()
    duracao7 = forms.CharField()
    duracao8 = forms.CharField()
    duracao9 = forms.CharField()
    duracao10 = forms.CharField()

    material = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    material2 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    material3 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    material4 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    material5 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    material6 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    material7 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    material8 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    material9 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)
    material10 = forms.CharField(label='Descrição', max_length=300, required=True, widget=forms.Textarea)


    data_inicial = forms.DateField()
    data_real = forms.DateField()
    data_final = forms.DateField()

    #Executores
    #Row 5
    executor1 = forms.ModelChoiceField(queryset=Pessoa.objects.all())
    porcento1 = forms.DecimalField()
    executor2 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    porcento2 = forms.DecimalField(required=False)
    executor3 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    porcento3 = forms.DecimalField(required=False)
    executor4 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    porcento4 = forms.DecimalField(required=False)
    executor5 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    porcento5 = forms.DecimalField(required=False)
    executor6 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    porcento6 = forms.DecimalField(required=False)
    executor7 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    porcento7 = forms.DecimalField(required=False)
    executor8 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    porcento8 = forms.DecimalField(required=False)
    executor9 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    porcento9 = forms.DecimalField(required=False)
    executor10 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    porcento10 = forms.DecimalField(required=False)


    # id_tamanho = forms.ModelChoiceField(queryset=Tamanho.objects.all())

    def __init__(self, *args, **kwargs):
        super(SolicitacaoForms, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        # self.fields['id_centro_custo'].queryset = CentroCusto.objects.all()
        # self.fields['id_centro_custo'].label_from_instance = lambda obj:(obj.centrocusto)


    class Meta:
        model = Solicitacao
        fields = '__all__'

class ExecutorForms(forms.ModelForm):
    
    id_tarefa = forms.IntegerField(required=False)
    executor1 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=True)
    executor2 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    executor3 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    executor4 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    executor5 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    executor6 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    executor7 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    executor8 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    executor9 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)
    executor10 = forms.ModelChoiceField(queryset=Pessoa.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(ExecutorForms, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work

        self.fields['executor1'].queryset = Pessoa.objects.all()
        self.fields['executor1'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor2'].queryset = Pessoa.objects.all()
        self.fields['executor2'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor3'].queryset = Pessoa.objects.all()
        self.fields['executor3'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor4'].queryset = Pessoa.objects.all()
        self.fields['executor4'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor5'].queryset = Pessoa.objects.all()
        self.fields['executor5'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor6'].queryset = Pessoa.objects.all()
        self.fields['executor6'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor7'].queryset = Pessoa.objects.all()
        self.fields['executor7'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor8'].queryset = Pessoa.objects.all()
        self.fields['executor8'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor9'].queryset = Pessoa.objects.all()
        self.fields['executor9'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor10'].queryset = Pessoa.objects.all()
        self.fields['executor10'].label_from_instance = lambda obj:(obj.nome)

    class Meta:
        model = Executor
        fields = '__all__'