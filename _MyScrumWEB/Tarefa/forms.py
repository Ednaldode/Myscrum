# Imports do Django
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext as _

# Imports do mesmo App
from .models import Tarefa, Executor, Retrospectiva, R5w2h

# Imports de outros Apps
from _Login.models import Pessoa
from Solicitacao.models import Solicitacao, Problema
from Fluxo.models import Locacao, Juridico, Testemunhas, Autor, Reu, Advocacia
from Departamento.models import Departamento
from Centro_de_custo.models import CentroCusto
from Tamanho.models import Tamanho
from Etapa.models import Etapas
from Sub_etapa.models import SubEtapas
from Processo.models import Processos
from _Login.views import get_user

# Import Biblioteca Python
import datetime

class TarefaForms(forms.ModelForm):
    STATUS_CHOICES = (
    ('A fazer', _("A fazer")),
    ('Fazendo', _("Fazendo")),
    ('Feito', _("Feito")),
    ('Cancelado', _("Cancelado"))
    )

    R5W2H_CHOICES = (
    (0, _("---------")),
    (1, _("Sim")),
    )

    RETROSPECTIVA_CHOICES = (
    (0, _("---------")),
    ('Foi bom', _("Foi bom")),
    ('Pode melhorar', _("Pode melhorar")),
    ('Deve melhorar', _("Deve melhorar")),
    )

    RSTATUS_CHOICES = (
    ('A fazer', _("A fazer")),
    ('Fazendo', _("Fazendo")),
    ('Feito', _("Feito"))
    )

    CALENDARIO_CHOICES = (
    ('0', _("Não")),
    ('1', _("Sim"))
    )

    MEDICAO_TERCEIROS_CHOICES = (
    (0, _("---------")),
    (1, _("Elaboração")),
    (2, _("Validação")),
    (3, _("Documentação")),
    (4, _("Nota Fiscal")),
    (5, _("Titulo a pagar")),
    )

    # Row 1
    id_tarefa = forms.IntegerField(required=False)
    descri = forms.CharField(label='Descrição', max_length=1000, required=False, widget=forms.Textarea)
    stat = forms.ChoiceField(choices=STATUS_CHOICES)
    rStat = forms.ChoiceField(choices=RSTATUS_CHOICES, required=False)
    prioridade = forms.ChoiceField(choices=[(x, x) for x in range(0, 8)])

    # Row 2
    data_ini = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}))
    data_real = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}))
    data_fim = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}))
    data_finalizacao = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}))
    data_finalizacao_sat = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}), required=False)
    id_tamanho = forms.ModelChoiceField(queryset=Tamanho.objects.all())
    porcentagem = forms.DecimalField()

    # Row 3
    id_departamento = forms.ModelChoiceField(queryset=Departamento.objects.all())
    id_centro_custo = forms.ModelChoiceField(queryset=CentroCusto.objects.all())
    id_centro_custo1 = forms.ModelChoiceField(queryset=CentroCusto.objects.all(), required=False)
    etapa = forms.ModelChoiceField(queryset=Etapas.objects.all(), required=False)
    subetapa = forms.ModelChoiceField(queryset=SubEtapas.objects.all(), required=False)

    # Row 4
    responsavel = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1))
    autoridade = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1))
    checado = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)

    # Row 5
    r5w2hT = forms.ChoiceField(choices=R5W2H_CHOICES, required=False)
    retrospec = forms.ChoiceField(choices=RETROSPECTIVA_CHOICES, required=False)
    calendario = forms.ChoiceField(choices=CALENDARIO_CHOICES, required=False)
    data_calendario = forms.DateTimeField(required=False)

    # Row 6
    historico = forms.CharField(required=False)
    status_pendencia = forms.CharField(required=False)

    # Row 6
    processo_relacionado = forms.ModelChoiceField(queryset=Processos.objects.all())
    pendente_por = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1),required=False)

    # Row 8
    id_medicao = forms.ChoiceField(choices=MEDICAO_TERCEIROS_CHOICES,required=False)

    # Campos preenchidos direto no banco
    id_empresa = forms.IntegerField(required=False)
    id_pessoa = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1))
    id_update = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1))
    last_update = forms.DateTimeField(required=False)
    id_locacao = forms.IntegerField(required=False)
    id_juridico = forms.IntegerField(required=False)

    #################################################################################

    # Retrospectiva

    id_responsavel = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    retrospectiva = forms.ChoiceField(choices=RETROSPECTIVA_CHOICES, required=False)
    r_historico = forms.CharField(required=False)
    finalizado = forms.IntegerField(required=False)

    #predecessor_1 = models.ForeignKey('self', models.DO_NOTHING, db_column='predecessor_1', blank=True, null=True, related_name='Predecessor_1')
    #predecessor_2 = models.ForeignKey('self', models.DO_NOTHING, db_column='predecessor_2', blank=True, null=True, related_name='Predecessor_2')
    #predecessor_3 = models.ForeignKey('self', models.DO_NOTHING, db_column='predecessor_3', blank=True, null=True, related_name='Predecessor_3')
    #anexo1 = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='anexo1', blank=True, null=True, related_name='Anexo1')
    #anexo2 = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='anexo2', blank=True, null=True, related_name='Anexo2')
    #anexo3 = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='anexo3', blank=True, null=True, related_name='Anexo3')
    #anexo4 = models.ForeignKey(Arquivos, models.DO_NOTHING, db_column='anexo4', blank=True, null=True, related_name='Anexo4')

    # Campos não usados
    #dpto_correto = forms.CharField(required=False)

    def __init__(self, request, *args, **kwargs):
        super(TarefaForms, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        usuario = get_user(request.user)

        self.fields['id_centro_custo'].queryset = CentroCusto.objects.filter(id_empresa=usuario.id_empresa)
        self.fields['id_centro_custo'].label_from_instance = lambda obj:(obj.centrocusto)
        
        self.fields['id_centro_custo1'].queryset = CentroCusto.objects.filter(id_empresa=usuario.id_empresa)
        self.fields['id_centro_custo1'].label_from_instance = lambda obj:(obj.centrocusto)

        self.fields['id_tamanho'].queryset = Tamanho.objects.all()
        self.fields['id_tamanho'].label_from_instance = lambda obj:(obj.descricao)

        self.fields['id_departamento'].queryset = Departamento.objects.filter(id_empresa=usuario.id_empresa)
        self.fields['id_departamento'].label_from_instance = lambda obj:(obj.departamento)

        self.fields['etapa'].queryset = Etapas.objects.filter(id_empresa=usuario.id_empresa)
        self.fields['etapa'].label_from_instance = lambda obj:(obj.etapa)

        self.fields['subetapa'].queryset = SubEtapas.objects.filter(id_empresa=usuario.id_empresa)
        self.fields['subetapa'].label_from_instance = lambda obj:(obj.sub_etapa)

        self.fields['processo_relacionado'].queryset = Processos.objects.filter(id_empresa=usuario.id_empresa)
        self.fields['processo_relacionado'].label_from_instance = lambda obj:(obj.processo)

        self.fields['responsavel'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['responsavel'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_responsavel'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['id_responsavel'].label_from_instance = lambda obj:(obj.nome)

        self.fields['autoridade'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['autoridade'].label_from_instance = lambda obj:(obj.nome)

        self.fields['checado'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['checado'].label_from_instance = lambda obj:(obj.nome)

        self.fields['pendente_por'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['pendente_por'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_pessoa'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['id_pessoa'].label_from_instance = lambda obj:(obj.nome)

        self.fields['id_update'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['id_update'].label_from_instance = lambda obj:(obj.nome)

    class Meta:
        model = Tarefa
        fields = '__all__'

class ExecutorFormsEditar(forms.ModelForm):
    executor1 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor2 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor3 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor4 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor5 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor6 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor7 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor8 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor9 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor10 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    def __init__(self, request, *args, **kwargs):
        super(ExecutorFormsEditar, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        usuario = get_user(request.user)

        self.fields['executor1'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor1'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor2'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor2'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor3'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor3'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor4'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor4'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor5'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor5'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor6'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor6'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor7'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor7'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor8'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor8'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor9'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor9'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor10'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor10'].label_from_instance = lambda obj:(obj.nome)

    class Meta:
        model = Executor
        fields = '__all__'

class ExecutorForms(forms.ModelForm):
    id_tarefa = forms.IntegerField(required=False)
    executor1 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor2 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor3 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor4 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor5 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor6 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor7 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor8 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor9 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    executor10 = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)

    def __init__(self, request, *args, **kwargs):
        super(ExecutorForms, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        usuario = get_user(request.user)

        self.fields['executor1'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor1'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor2'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor2'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor3'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor3'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor4'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor4'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor5'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor5'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor6'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor6'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor7'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor7'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor8'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor8'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor9'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor9'].label_from_instance = lambda obj:(obj.nome)

        self.fields['executor10'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['executor10'].label_from_instance = lambda obj:(obj.nome)

    class Meta:
        model = Executor
        fields = '__all__'

class SolicitacaoForms(forms.ModelForm):
    STATUS_CHOICES = (
    ('A fazer', _("A fazer")),
    ('Fazendo', _("Fazendo")),
    ('Feito', _("Feito")),
    ('Cancelado', _("Cancelado"))
    )

    SOLICITACAO_CHOICES = (
    ('Vistoria de Entrega', _("Vistoria de Entrega")),
    ('Garantia', _("Garantia")),
    )

    PROCESSO_CHOICES = (
    ('Análise', _("Análise")),
    ('Agendamento', _("Agendamento")),
    ('Atendimento', _("Atendimento")),
    ('Termo de Quitação', _("Termo de Quitação")),
    ('Concluído', _("Concluído")),
    ('Fora de Garantia', _("Fora de Garantia")),
    ('Cancelado', _("Cancelado")),
    )

    AVALIACAO_CHOICES = (
    ('5', _("Sem Avaliação")),
    ('1', _("Ruim")),
    ('2', _("Regular")),
    ('3', _("Bom")),
    ('4', _("Ótimo")),
    )
    
    EMPREENDIMENTO_CHOICES = (
    ('', _("---")),
    ('Le Jardin', _("Le Jardin")),
    ('Villa Helvétia', _("Villa Helvétia")),
    ('Villa Unitá', _("Villa Unitá")),
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
    ('Container', _("Container")),
    ('Casa de Sócios', _("Casa de Sócios")),
    ('Escritório', _("Escritório")),
    ('Central de Vendas', _("Central de Vendas")),
    )

    BLOCOS_CHOICES = (
    ('', _("---")),
    ('Área Comum', _("Área Comum")),
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
    ('Outros', _("Outros")),
    ('Terceiro', _("Terceiro")),
    # ('II', _("II")),
    # ('III', _("III")),
    # ('IV', _("IV")),
    # ('V', _("V")),
    # ('VI', _("VI")),
    # ('VII', _("VII")),
    # ('CANNES', _("CANNES")),
    # ('LYON', _("LYON")),
    # ('BOURDEAUX', _("BOURDEAUX")),
    )

    id_solicitacao = forms.IntegerField(required=False)
    id_tarefa = forms.IntegerField(required=False)
    empreendimento = forms.ChoiceField(choices=EMPREENDIMENTO_CHOICES, required=False)
    bloco = forms.ChoiceField(choices=BLOCOS_CHOICES, required=False)
    unidade = forms.CharField(required=False)
    proprietario_nome = forms.CharField(required=False)
    proprietario_nome1 = forms.CharField(required=False)
    proprietario_rg = forms.CharField(required=False)
    proprietario_cpf = forms.CharField(required=False)
    proprietario_email = forms.CharField(required=False)
    solicitante_nome = forms.CharField(required=False)
    solicitante_rg = forms.CharField(required=False)
    solicitante_cpf = forms.CharField(required=False)
    solicitante_email = forms.CharField(required=False)
    telefone1 = forms.CharField(required=False)
    telefone2 = forms.CharField(required=False)
    status_processo = forms.ChoiceField(choices=PROCESSO_CHOICES, required=False)
    status_solicitacao = forms.CharField(required=False)
    satisfacao_avaliacao = forms.ChoiceField(choices=AVALIACAO_CHOICES, required=False)
    data_abertura = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}), required=False)
    data_atendimento = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}), required=False)
    data_finalizacao_sat = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}), required=False)
    data_entrega = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}), required=False)
    tipo_solicitacao = forms.ChoiceField(choices=SOLICITACAO_CHOICES, required=False)
    tempo_total = forms.ModelChoiceField(queryset=Tamanho.objects.all(), required=False)

    responsavel_sat = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    autoridade_sat = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    porcentagem_sat = forms.CharField(required=False)
    processo_relacionado_sat = forms.ModelChoiceField(queryset=Processos.objects.all(), required=False)

    def __init__(self, request, *args, **kwargs):
        super(SolicitacaoForms, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        usuario = get_user(request.user)

        self.fields['responsavel_sat'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['responsavel_sat'].label_from_instance = lambda obj:(obj.nome)

        self.fields['autoridade_sat'].queryset = Pessoa.objects.filter(ativo=1)
        self.fields['autoridade_sat'].label_from_instance = lambda obj:(obj.nome)

        self.fields['processo_relacionado_sat'].queryset = Processos.objects.filter(id_empresa=usuario.id_empresa)
        self.fields['processo_relacionado_sat'].label_from_instance = lambda obj:(obj.processo)

        self.fields['tempo_total'].queryset = Tamanho.objects.all()
        self.fields['tempo_total'].label_from_instance = lambda obj:(obj.descricao)

    class Meta:
        model = Solicitacao
        fields = '__all__'

class LocacaoForms(forms.ModelForm):
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
        ('K', _("K"))
    )

    lBloco = forms.ChoiceField(choices=BLOCOS_CHOICES, required=False)
    lUnidade = forms.CharField(required=False)

    class Meta:
        model = Locacao
        fields = '__all__'

class JuridicoForms(forms.ModelForm):
    BLOCOS_CHOICES = (
    ('', _("---")),
    ('Área Comum', _("Área Comum")),
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
    ('Terceiro', _("Terceiro")),
    )

    numero_processo = forms.CharField(required=False)
    escritorio = forms.ModelChoiceField(queryset=Advocacia.objects.all())
    escritorio_advogado = forms.ModelChoiceField(queryset=Pessoa.objects.exclude(id_advocacia=None), required=False)
    resumo_processo = forms.CharField(label='Descrição', max_length=1000, required=False, widget=forms.Textarea)
    autor_assistente = forms.CharField(required=False)
    autor_advogado = forms.CharField(required=False)
    reu_assistente = forms.CharField(required=False)
    reu_advogado = forms.CharField(required=False)
    prazo_interno = forms.DateField(widget=forms.DateInput(attrs={'class': 'input--style-4 js-datepicker'}),required=False)
    observacoes = forms.CharField(label='Descrição', max_length=1000, required=False, widget=forms.Textarea)
    valor_estimado = forms.CharField(required=False)
    valor_causa = forms.CharField(required=False)
    valor_acordo = forms.CharField(required=False)
    perito = forms.CharField(required=False)
    preposto = forms.ModelChoiceField(queryset=Pessoa.objects.filter(ativo=1), required=False)
    jUnidade = forms.CharField(required=False)
    jBloco = forms.ChoiceField(choices=BLOCOS_CHOICES, required=False)

    def __init__(self, request, *args, **kwargs):
        super(JuridicoForms, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        usuario = get_user(request.user)

        self.fields['escritorio'].queryset = Advocacia.objects.filter(id_empresa=usuario.id_empresa)
        self.fields['escritorio'].label_from_instance = lambda obj:(obj.escritorio)

        self.fields['preposto'].queryset = Pessoa.objects.filter(ativo=1, id_empresa=usuario.id_empresa)
        self.fields['preposto'].label_from_instance = lambda obj:(obj.nome)

        self.fields['escritorio_advogado'].queryset = Pessoa.objects.filter(id_empresa=usuario.id_empresa).exclude(id_advocacia=None)
        self.fields['escritorio_advogado'].label_from_instance = lambda obj:(obj.nome)

    class Meta:
        model = Juridico
        fields = '__all__'

class TestemunhasForms(forms.ModelForm):
    testemunha1 = forms.CharField(required=False)
    testemunha2 = forms.CharField(required=False)
    testemunha3 = forms.CharField(required=False)
    testemunha4 = forms.CharField(required=False)
    testemunha5 = forms.CharField(required=False)
    testemunha6 = forms.CharField(required=False)
    testemunha7 = forms.CharField(required=False)
    testemunha8 = forms.CharField(required=False)
    testemunha9 = forms.CharField(required=False)
    testemunha10 = forms.CharField(required=False)

    class Meta:
        model = Testemunhas
        fields = '__all__'

class AutorForms(forms.ModelForm):
    autor1 = forms.CharField(required=False)
    autor2 = forms.CharField(required=False)
    autor3 = forms.CharField(required=False)
    autor4 = forms.CharField(required=False)
    autor5 = forms.CharField(required=False)
    autor6 = forms.CharField(required=False)
    autor7 = forms.CharField(required=False)
    autor8 = forms.CharField(required=False)
    autor9 = forms.CharField(required=False)
    autor10 = forms.CharField(required=False)

    class Meta:
        model = Autor
        fields = '__all__'

class ReuForms(forms.ModelForm):
    reu1 = forms.CharField(required=False)
    reu2 = forms.CharField(required=False)
    reu3 = forms.CharField(required=False)
    reu4 = forms.CharField(required=False)
    reu5 = forms.CharField(required=False)
    reu6 = forms.CharField(required=False)
    reu7 = forms.CharField(required=False)
    reu8 = forms.CharField(required=False)
    reu9 = forms.CharField(required=False)
    reu10 = forms.CharField(required=False)

    class Meta:
        model = Reu
        fields = '__all__'
