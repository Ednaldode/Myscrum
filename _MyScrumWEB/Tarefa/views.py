# Import Django
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage, File 
from pprint import pprint
# Import de outros Apps
from _Login.models import Pessoa, Vinculos
from Departamento.models import Departamento
from Centro_de_custo.models import CentroCusto
from Tamanho.models import Tamanho
from Etapa.models import Etapas
from Sub_etapa.models import SubEtapas
from Processo.models import Processos
from Fluxo.models import Locacao, LocacaoEditar, FluxoLocacao, MedicaoTerceiros, Juridico, Testemunhas, Autor, Reu
from Fluxo.forms import EditarMedicaoTerceiros
from _Login.views import get_user
from Solicitacao.models import Solicitacao, Problema
from Kanban.models import TarefasKanban
from _MyScrumWEB import urls

# Import de mesmo App
from .models import Tarefa, Executor, ListarTarefas, Retrospectiva, R5w2h, ExportarTarefas
from .forms import TarefaForms, ExecutorForms, ExecutorFormsEditar, SolicitacaoForms, LocacaoForms, JuridicoForms, TestemunhasForms, AutorForms, ReuForms

# Import Biblioteca Python
from datetime import date, datetime, timedelta
import json
import xlrd
import xlwt
import os

# Create your views here.

# Tarefas #
@login_required(login_url=urls.getUrlSubdominio())
def listarTarefas(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    tarefas = ListarTarefas.objects.extra(where=[filtrosWhere['WHERE']]).order_by('prioridade')

    pessoas = Pessoa.objects.all()
    departamentos = Departamento.objects.all()
    centrocustos = CentroCusto.objects.all()
    processos = Processos.objects.all()

    if request.GET.get('centrocusto') != 'Centros de custo':
        etapas = Etapas.objects.filter(id_cc=request.GET.get('centrocusto'))
    else:
        etapas = ''

    if request.GET.get('etapa') != 'Etapas':
        subetapas = SubEtapas.objects.filter(id_etapa=request.GET.get('etapa'))
    else:
        subetapas = ''

    context = {
        'tarefas' : tarefas,
        'pessoas' : pessoas,
        'departamentos' : departamentos,
        'centrocustos' : centrocustos,
        'etapas' : etapas,
        'subetapas' : subetapas,
        'processos' : processos,
        'filtros' : filtrosWhere['filtros'],
        'r5w2hT' : filtrosWhere['r5w2hT'],
        'usuario' : usuario,
        'status' : filtrosWhere['status'],
    }

    return render(request, 'listarTarefas.html', context)

@login_required(login_url=urls.getUrlSubdominio())
def cadastrarTarefas(request):
    usuario = get_user(request.user)

    retrospectiva = ""
    r5w2h = ""

    solicitacao = ""
    problema = ""        
    solicitacao_form = SolicitacaoForms(request)

    medicao_terceiros = ""
    medicao_terceiros_form = EditarMedicaoTerceiros()

    locacao = ""
    locacao_form = LocacaoForms()

    juridico = ""
    juridico_form = JuridicoForms(request)

    testemunhas = ""
    testemunhas_form = TestemunhasForms()

    autor = ""
    autor_form = AutorForms()
    
    reu = ""
    reu_form = ReuForms()

    if request.method == 'POST':
        form = TarefaForms(request, request.POST)
        executores_form = ExecutorForms(request, request.POST)
        
        calendario = None
        data_calendario = None

        if request.POST['calendario'] == '1':
            calendario = 1
            data_calendario = "{}-00:00".format(request.POST['data_calendario'])
        
        # Tarefas #
        if form.is_valid():
            if form.cleaned_data['processo_relacionado'].id_processo == 63:
                tarefa = Tarefa(
                    id_empresa = usuario.id_empresa,
                    descri = form.cleaned_data['descri'],
                    id_centro_custo = form.cleaned_data['id_centro_custo'],
                    prioridade = form.cleaned_data['prioridade'],
                    stat = form.cleaned_data['stat'],
                    id_tamanho = form.cleaned_data['id_tamanho'],
                    porcentagem = form.cleaned_data['porcentagem'],
                    prazo = form.cleaned_data['prazo'],
                    data_ini = form.cleaned_data['data_ini'],
                    data_real = form.cleaned_data['data_real'],
                    data_fim = form.cleaned_data['data_fim'],
                    data_finalizacao = form.cleaned_data['data_finalizacao'],
                    pendente_por = form.cleaned_data['pendente_por'],
                    status_pendencia = form.cleaned_data['status_pendencia'],
                    historico = form.cleaned_data['historico'],
                    id_departamento = form.cleaned_data['id_departamento'],
                    responsavel = form.cleaned_data['responsavel'],
                    autoridade = form.cleaned_data['autoridade'],
                    processo_relacionado = form.cleaned_data['processo_relacionado'],
                    id_pessoa = form.cleaned_data['id_pessoa'],
                    last_update = datetime.now(),
                    id_update = form.cleaned_data['id_update'],
                    checado = form.cleaned_data['checado'],
                    etapa = form.cleaned_data['etapa'],
                    subetapa = form.cleaned_data['subetapa'],
                    retrospec = form.cleaned_data['retrospec'],
                    calendario = calendario,
                    data_calendario = data_calendario,
                    id_status = 0,
                )
                tarefa.save()

                id_locacao = tarefa.id_tarefa
                tarefa.id_locacao = id_locacao
                tarefa.save()

                # Executores #
                if executores_form.is_valid():
                    new_executores = Executor(
                        executor1 = executores_form.cleaned_data['executor1'],
                        porcento1 = executores_form.cleaned_data['porcento1'],
                        executor2 = executores_form.cleaned_data['executor2'],
                        porcento2 = executores_form.cleaned_data['porcento2'],
                        executor3 = executores_form.cleaned_data['executor3'],
                        porcento3 = executores_form.cleaned_data['porcento3'],
                        executor4 = executores_form.cleaned_data['executor4'],
                        porcento4 = executores_form.cleaned_data['porcento4'],
                        executor5 = executores_form.cleaned_data['executor5'],
                        porcento5 = executores_form.cleaned_data['porcento5'],
                        executor6 = executores_form.cleaned_data['executor6'],
                        porcento6 = executores_form.cleaned_data['porcento6'],
                        executor7 = executores_form.cleaned_data['executor7'],
                        porcento7 = executores_form.cleaned_data['porcento7'],
                        executor8 = executores_form.cleaned_data['executor8'],
                        porcento8 = executores_form.cleaned_data['porcento8'],
                        executor9 = executores_form.cleaned_data['executor9'],
                        porcento9 = executores_form.cleaned_data['porcento9'],
                        executor10 = executores_form.cleaned_data['executor10'],
                        porcento10 = executores_form.cleaned_data['porcento10'],
                        id_tarefa = Tarefa.objects.get(pk=tarefa.id_tarefa),
                    )

                    new_executores.save()
                else:
                    context = {
                        'form' : form,
                        'executores_form' : executores_form,
                        'usuario' : usuario
                    }
                    messages.success(request, 'Falha ao cadastrar a tarefa!', extra_tags='danger')
                    return render(request, 'cadastrarTarefas.html', context)

                ambientes = []
                listaAmbiente = request.POST.getlist('ambientes')
                for lAmbiente in listaAmbiente:
                    try:
                        aux = lAmbiente.split(" | ")
                        orcar = aux[0]
                        ambiente = aux[1]
                    except:
                        orcar = lAmbiente
                    index = [i for i, elem in enumerate(ambientes) if orcar in elem]
                    if (index):
                        ambientes[index[0]] += " - " + ambiente
                    else:
                        ambientes.append(orcar + ' - ' + ambiente)

                # Busca dados da tarefa mãe
                id_locacao = tarefa.id_locacao
                locacao_padrao = get_object_or_404(LocacaoEditar, id_locacao_editar=3)

                # Nova tarefa # - Ligação de energia
                new_tarefa = Tarefa(
                    id_empresa = usuario.id_empresa,
                    descri = locacao_padrao.descricao + " " + str(id_locacao) + " - " + tarefa.descri,
                    id_centro_custo = tarefa.id_centro_custo,
                    prioridade = tarefa.prioridade,
                    stat = "A fazer",
                    id_tamanho = locacao_padrao.id_tamanho,
                    porcentagem = 0,
                    prazo = locacao_padrao.prazo,
                    data_ini = tarefa.data_fim - timedelta(days = 10),
                    data_real = tarefa.data_fim - timedelta(days = 10),
                    # Acrescenta +3 dias a partir da finalização da anterior.
                    data_fim = tarefa.data_fim + timedelta(days = locacao_padrao.prazo),
                    data_finalizacao = tarefa.data_finalizacao,
                    data_finalizacao_sat = tarefa.data_finalizacao_sat,
                    status_pendencia = locacao_padrao.status_pendencia,
                    historico = "",
                    id_departamento = locacao_padrao.id_departamento,
                    responsavel = locacao_padrao.id_responsavel,
                    autoridade = locacao_padrao.id_autoridade,
                    processo_relacionado = tarefa.processo_relacionado,
                    id_pessoa = tarefa.id_pessoa,
                    last_update = datetime.now(),
                    id_update = tarefa.id_update,
                    checado = locacao_padrao.id_checado,
                    pendente_por = locacao_padrao.id_pendente_por,
                    etapa = tarefa.etapa,
                    subetapa = tarefa.subetapa,
                    retrospec = tarefa.retrospec,
                    id_locacao = id_locacao,
                    id_status = 3,
                )
                new_tarefa.save()

                # Executores #
                new_executores = Executor(
                    executor1 = locacao_padrao.id_executor1,
                    porcento1 = locacao_padrao.porcento1,
                    executor2 = locacao_padrao.id_executor2,
                    porcento2 = locacao_padrao.porcento2,
                    executor3 = locacao_padrao.id_executor3,
                    porcento3 = locacao_padrao.porcento3,
                    executor4 = locacao_padrao.id_executor4,
                    porcento4 = locacao_padrao.porcento4,
                    executor5 = locacao_padrao.id_executor5,
                    porcento5 = locacao_padrao.porcento5,
                    executor6 = locacao_padrao.id_executor6,
                    porcento6 = locacao_padrao.porcento6,
                    executor7 = locacao_padrao.id_executor7,
                    porcento7 = locacao_padrao.porcento7,
                    executor8 = locacao_padrao.id_executor8,
                    porcento8 = locacao_padrao.porcento8,
                    executor9 = locacao_padrao.id_executor9,
                    porcento9 = locacao_padrao.porcento9,
                    executor10 = locacao_padrao.id_executor10,
                    porcento10 = locacao_padrao.porcento10,
                    id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                )
                new_executores.save()
                
                # Nova tarefa # - Orçar
                locacao_padrao = get_object_or_404(LocacaoEditar, id_locacao_editar=4)
                for ambiente in ambientes:
                    ambiente1 = ambiente.split(" - ")
                    # Nova tarefa # - Orçar
                    new_tarefa = Tarefa(
                        id_empresa = usuario.id_empresa,
                        descri = locacao_padrao.descricao + " " + ambiente1[0] + " - " + str(id_locacao) + " - " + tarefa.descri,
                        id_centro_custo = tarefa.id_centro_custo,
                        prioridade = tarefa.prioridade,
                        stat = "A fazer",
                        id_tamanho = locacao_padrao.id_tamanho,
                        porcentagem = 0,
                        prazo = locacao_padrao.prazo,
                        data_ini = tarefa.data_ini + timedelta(days = 3),
                        data_real = tarefa.data_ini + timedelta(days = 3),
                        # Acrescenta +3 dias a partir da finalização da anterior.
                        data_fim = tarefa.data_ini + timedelta(days = 3) + timedelta(days = locacao_padrao.prazo),
                        data_finalizacao = tarefa.data_finalizacao,
                        data_finalizacao_sat = tarefa.data_finalizacao_sat,
                        status_pendencia = locacao_padrao.status_pendencia + " - " + ambiente,
                        historico = "",
                        id_departamento = locacao_padrao.id_departamento,
                        responsavel = locacao_padrao.id_responsavel,
                        autoridade = locacao_padrao.id_autoridade,
                        processo_relacionado = tarefa.processo_relacionado,
                        id_pessoa = tarefa.id_pessoa,
                        last_update = datetime.now(),
                        id_update = tarefa.id_update,
                        checado = locacao_padrao.id_checado,
                        pendente_por = locacao_padrao.id_pendente_por,
                        etapa = tarefa.etapa,
                        subetapa = tarefa.subetapa,
                        retrospec = tarefa.retrospec,
                        id_locacao = id_locacao,
                        id_status = 4,
                    )
                    new_tarefa.save()

                        # Executores #
                    new_executores = Executor(
                        executor1 = locacao_padrao.id_executor1,
                        porcento1 = locacao_padrao.porcento1,
                        executor2 = locacao_padrao.id_executor2,
                        porcento2 = locacao_padrao.porcento2,
                        executor3 = locacao_padrao.id_executor3,
                        porcento3 = locacao_padrao.porcento3,
                        executor4 = locacao_padrao.id_executor4,
                        porcento4 = locacao_padrao.porcento4,
                        executor5 = locacao_padrao.id_executor5,
                        porcento5 = locacao_padrao.porcento5,
                        executor6 = locacao_padrao.id_executor6,
                        porcento6 = locacao_padrao.porcento6,
                        executor7 = locacao_padrao.id_executor7,
                        porcento7 = locacao_padrao.porcento7,
                        executor8 = locacao_padrao.id_executor8,
                        porcento8 = locacao_padrao.porcento8,
                        executor9 = locacao_padrao.id_executor9,
                        porcento9 = locacao_padrao.porcento9,
                        executor10 = locacao_padrao.id_executor10,
                        porcento10 = locacao_padrao.porcento10,
                        id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                    )
                    new_executores.save()

                # Nova tarefa # - Limpeza
                locacao_padrao = get_object_or_404(LocacaoEditar, id_locacao_editar=7)
                new_tarefa = Tarefa(
                    id_empresa = usuario.id_empresa,
                    descri = locacao_padrao.descricao + " " + str(id_locacao) + " - " + tarefa.descri,
                    id_centro_custo = tarefa.id_centro_custo,
                    prioridade = tarefa.prioridade,
                    stat = "A fazer",
                    id_tamanho = locacao_padrao.id_tamanho,
                    porcentagem = 0,
                    prazo = locacao_padrao.prazo,
                    data_ini = tarefa.data_fim - timedelta(days = 3),
                    data_real = tarefa.data_fim - timedelta(days = 3),
                    # Acrescenta +3 dias a partir da finalização da anterior.
                    data_fim = tarefa.data_fim + timedelta(days = 3),
                    data_finalizacao = tarefa.data_finalizacao,
                    data_finalizacao_sat = tarefa.data_finalizacao_sat,
                    status_pendencia = locacao_padrao.status_pendencia,
                    historico = "",
                    id_departamento = locacao_padrao.id_departamento,
                    responsavel = locacao_padrao.id_responsavel,
                    autoridade = locacao_padrao.id_autoridade,
                    processo_relacionado = tarefa.processo_relacionado,
                    id_pessoa = tarefa.id_pessoa,
                    last_update = datetime.now(),
                    id_update = tarefa.id_update,
                    checado = locacao_padrao.id_checado,
                    pendente_por = locacao_padrao.id_pendente_por,
                    etapa = tarefa.etapa,
                    subetapa = tarefa.subetapa,
                    retrospec = tarefa.retrospec,
                    id_locacao = id_locacao,
                    id_status = 7,
                )
                new_tarefa.save()

                # Executores #
                new_executores = Executor(
                    executor1 = locacao_padrao.id_executor1,
                    porcento1 = locacao_padrao.porcento1,
                    executor2 = locacao_padrao.id_executor2,
                    porcento2 = locacao_padrao.porcento2,
                    executor3 = locacao_padrao.id_executor3,
                    porcento3 = locacao_padrao.porcento3,
                    executor4 = locacao_padrao.id_executor4,
                    porcento4 = locacao_padrao.porcento4,
                    executor5 = locacao_padrao.id_executor5,
                    porcento5 = locacao_padrao.porcento5,
                    executor6 = locacao_padrao.id_executor6,
                    porcento6 = locacao_padrao.porcento6,
                    executor7 = locacao_padrao.id_executor7,
                    porcento7 = locacao_padrao.porcento7,
                    executor8 = locacao_padrao.id_executor8,
                    porcento8 = locacao_padrao.porcento8,
                    executor9 = locacao_padrao.id_executor9,
                    porcento9 = locacao_padrao.porcento9,
                    executor10 = locacao_padrao.id_executor10,
                    porcento10 = locacao_padrao.porcento10,
                    id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                )
                new_executores.save()
               
                if (locacao == ""):
                    if (request.POST['lBloco'] != "---"):
                        bloco = request.POST['lBloco']
                        unidade = request.POST['lUnidade']

                        tarefa.id_locacao = tarefa.id_tarefa
                        tarefa.save()

                        locacao = Locacao(id_tarefa=tarefa.id_locacao, lBloco=bloco, lUnidade=unidade, id_empresa = usuario.id_empresa)
                        locacao.save()
                    else:
                        print("Não há locacao")
                else:
                    if (tarefa.id_locacao != None):
                        locacao = get_object_or_404(Locacao, id_tarefa=request.POST['id_locacao'])
                        locacao.id_tarefa = tarefa.id_tarefa
                        locacao.lBloco = request.POST['lBloco']
                        locacao.lUnidade = request.POST['lUnidade']

                        tarefa.id_locacao = tarefa.id_tarefa
                        tarefa.save()

                        locacao.save()
            elif form.cleaned_data['processo_relacionado'].id_processo == 146:
                tarefa = Tarefa(
                    id_empresa = usuario.id_empresa,
                    descri = form.cleaned_data['descri'],
                    id_centro_custo = form.cleaned_data['id_centro_custo'],
                    prioridade = form.cleaned_data['prioridade'],
                    stat = form.cleaned_data['stat'],
                    id_tamanho = form.cleaned_data['id_tamanho'],
                    porcentagem = form.cleaned_data['porcentagem'],
                    prazo = form.cleaned_data['prazo'],
                    data_ini = form.cleaned_data['data_ini'],
                    data_real = form.cleaned_data['data_real'],
                    data_fim = form.cleaned_data['data_fim'],
                    data_finalizacao = form.cleaned_data['data_finalizacao'],
                    pendente_por = form.cleaned_data['pendente_por'],
                    status_pendencia = form.cleaned_data['status_pendencia'],
                    historico = form.cleaned_data['historico'],
                    id_departamento = form.cleaned_data['id_departamento'],
                    responsavel = form.cleaned_data['responsavel'],
                    autoridade = form.cleaned_data['autoridade'],
                    processo_relacionado = form.cleaned_data['processo_relacionado'],
                    id_pessoa = form.cleaned_data['id_pessoa'],
                    last_update = datetime.now(),
                    id_update = form.cleaned_data['id_update'],
                    checado = form.cleaned_data['checado'],
                    etapa = form.cleaned_data['etapa'],
                    subetapa = form.cleaned_data['subetapa'],
                    retrospec = form.cleaned_data['retrospec'],
                    calendario = calendario,
                    data_calendario = data_calendario,
                    id_status = 11,
                )
                tarefa.save()

                id_locacao = tarefa.id_tarefa
                tarefa.id_locacao = id_locacao
                tarefa.save()

                # Executores #
                if executores_form.is_valid():
                    new_executores = Executor(
                        executor1 = executores_form.cleaned_data['executor1'],
                        porcento1 = executores_form.cleaned_data['porcento1'],
                        executor2 = executores_form.cleaned_data['executor2'],
                        porcento2 = executores_form.cleaned_data['porcento2'],
                        executor3 = executores_form.cleaned_data['executor3'],
                        porcento3 = executores_form.cleaned_data['porcento3'],
                        executor4 = executores_form.cleaned_data['executor4'],
                        porcento4 = executores_form.cleaned_data['porcento4'],
                        executor5 = executores_form.cleaned_data['executor5'],
                        porcento5 = executores_form.cleaned_data['porcento5'],
                        executor6 = executores_form.cleaned_data['executor6'],
                        porcento6 = executores_form.cleaned_data['porcento6'],
                        executor7 = executores_form.cleaned_data['executor7'],
                        porcento7 = executores_form.cleaned_data['porcento7'],
                        executor8 = executores_form.cleaned_data['executor8'],
                        porcento8 = executores_form.cleaned_data['porcento8'],
                        executor9 = executores_form.cleaned_data['executor9'],
                        porcento9 = executores_form.cleaned_data['porcento9'],
                        executor10 = executores_form.cleaned_data['executor10'],
                        porcento10 = executores_form.cleaned_data['porcento10'],
                        id_tarefa = Tarefa.objects.get(pk=tarefa.id_tarefa),
                    )

                    new_executores.save()
                else:
                    context = {
                        'form' : form,
                        'executores_form' : executores_form,
                        'usuario' : usuario
                    }
                    messages.success(request, 'Falha ao cadastrar a tarefa!', extra_tags='danger')
                    return render(request, 'cadastrarTarefas.html', context)
            elif form.cleaned_data['processo_relacionado'].id_processo == 29:
                tarefa = Tarefa(
                    id_empresa = usuario.id_empresa,
                    descri = form.cleaned_data['descri'],
                    id_centro_custo = form.cleaned_data['id_centro_custo'],
                    prioridade = form.cleaned_data['prioridade'],
                    stat = form.cleaned_data['stat'],
                    id_tamanho = form.cleaned_data['id_tamanho'],
                    porcentagem = form.cleaned_data['porcentagem'],
                    prazo = form.cleaned_data['prazo'],
                    data_ini = form.cleaned_data['data_ini'],
                    data_real = form.cleaned_data['data_real'],
                    data_fim = form.cleaned_data['data_fim'],
                    data_finalizacao = form.cleaned_data['data_finalizacao'],
                    pendente_por = form.cleaned_data['pendente_por'],
                    status_pendencia = form.cleaned_data['status_pendencia'],
                    historico = form.cleaned_data['historico'],
                    id_departamento = form.cleaned_data['id_departamento'],
                    responsavel = form.cleaned_data['responsavel'],
                    autoridade = form.cleaned_data['autoridade'],
                    processo_relacionado = form.cleaned_data['processo_relacionado'],
                    id_pessoa = form.cleaned_data['id_pessoa'],
                    last_update = datetime.now(),
                    id_update = form.cleaned_data['id_update'],
                    checado = form.cleaned_data['checado'],
                    etapa = form.cleaned_data['etapa'],
                    subetapa = form.cleaned_data['subetapa'],
                    retrospec = form.cleaned_data['retrospec'],
                    calendario = calendario,
                    data_calendario = data_calendario,
                    id_status = 1,
                )
                tarefa.save()

                id_juridico = tarefa.id_tarefa

                tarefa.id_juridico = id_juridico
                tarefa.save()

                # Executores #
                if executores_form.is_valid():
                    new_executores = Executor(
                        executor1 = executores_form.cleaned_data['executor1'],
                        porcento1 = executores_form.cleaned_data['porcento1'],
                        executor2 = executores_form.cleaned_data['executor2'],
                        porcento2 = executores_form.cleaned_data['porcento2'],
                        executor3 = executores_form.cleaned_data['executor3'],
                        porcento3 = executores_form.cleaned_data['porcento3'],
                        executor4 = executores_form.cleaned_data['executor4'],
                        porcento4 = executores_form.cleaned_data['porcento4'],
                        executor5 = executores_form.cleaned_data['executor5'],
                        porcento5 = executores_form.cleaned_data['porcento5'],
                        executor6 = executores_form.cleaned_data['executor6'],
                        porcento6 = executores_form.cleaned_data['porcento6'],
                        executor7 = executores_form.cleaned_data['executor7'],
                        porcento7 = executores_form.cleaned_data['porcento7'],
                        executor8 = executores_form.cleaned_data['executor8'],
                        porcento8 = executores_form.cleaned_data['porcento8'],
                        executor9 = executores_form.cleaned_data['executor9'],
                        porcento9 = executores_form.cleaned_data['porcento9'],
                        executor10 = executores_form.cleaned_data['executor10'],
                        porcento10 = executores_form.cleaned_data['porcento10'],
                        id_tarefa = Tarefa.objects.get(pk=tarefa.id_tarefa),
                    )

                    new_executores.save()
                else:
                    context = {
                        'form' : form,
                        'executores_form' : executores_form,
                        'usuario' : usuario
                    }
                    messages.success(request, 'Falha ao cadastrar a tarefa!', extra_tags='danger')
                    return render(request, 'cadastrarTarefas.html', context)

                t1_tarefa = Tarefa(
                    id_empresa = usuario.id_empresa,
                    descri = "Petição Inicial: " + tarefa.descri,
                    id_centro_custo = form.cleaned_data['id_centro_custo'],
                    prioridade = form.cleaned_data['prioridade'],
                    stat = "A fazer",
                    id_tamanho = form.cleaned_data['id_tamanho'],
                    porcentagem = 0,
                    prazo = form.cleaned_data['prazo'],
                    data_ini = form.cleaned_data['data_ini'],
                    data_real = form.cleaned_data['data_real'],
                    data_fim = form.cleaned_data['data_fim'],
                    data_finalizacao = form.cleaned_data['data_finalizacao'],
                    pendente_por = form.cleaned_data['pendente_por'],
                    status_pendencia = "",
                    historico = "",
                    id_departamento = form.cleaned_data['id_departamento'],
                    responsavel = form.cleaned_data['responsavel'],
                    autoridade = form.cleaned_data['autoridade'],
                    processo_relacionado = form.cleaned_data['processo_relacionado'],
                    id_pessoa = form.cleaned_data['id_pessoa'],
                    last_update = datetime.now(),
                    id_update = form.cleaned_data['id_update'],
                    checado = form.cleaned_data['checado'],
                    etapa = form.cleaned_data['etapa'],
                    subetapa = form.cleaned_data['subetapa'],
                    retrospec = form.cleaned_data['retrospec'],
                    id_juridico = id_juridico,
                    id_status = 2,
                )
                t1_tarefa.save()

                t1_executores = Executor(
                    executor1 = executores_form.cleaned_data['executor1'],
                    porcento1 = executores_form.cleaned_data['porcento1'],
                    executor2 = executores_form.cleaned_data['executor2'],
                    porcento2 = executores_form.cleaned_data['porcento2'],
                    executor3 = executores_form.cleaned_data['executor3'],
                    porcento3 = executores_form.cleaned_data['porcento3'],
                    executor4 = executores_form.cleaned_data['executor4'],
                    porcento4 = executores_form.cleaned_data['porcento4'],
                    executor5 = executores_form.cleaned_data['executor5'],
                    porcento5 = executores_form.cleaned_data['porcento5'],
                    executor6 = executores_form.cleaned_data['executor6'],
                    porcento6 = executores_form.cleaned_data['porcento6'],
                    executor7 = executores_form.cleaned_data['executor7'],
                    porcento7 = executores_form.cleaned_data['porcento7'],
                    executor8 = executores_form.cleaned_data['executor8'],
                    porcento8 = executores_form.cleaned_data['porcento8'],
                    executor9 = executores_form.cleaned_data['executor9'],
                    porcento9 = executores_form.cleaned_data['porcento9'],
                    executor10 = executores_form.cleaned_data['executor10'],
                    porcento10 = executores_form.cleaned_data['porcento10'],
                    id_tarefa = Tarefa.objects.get(pk=t1_tarefa.id_tarefa),
                )

                t1_executores.save()
            else:
                tarefa = Tarefa(
                    id_empresa = usuario.id_empresa,
                    descri = form.cleaned_data['descri'],
                    id_centro_custo = form.cleaned_data['id_centro_custo'],
                    prioridade = form.cleaned_data['prioridade'],
                    stat = form.cleaned_data['stat'],
                    id_tamanho = form.cleaned_data['id_tamanho'],
                    porcentagem = form.cleaned_data['porcentagem'],
                    prazo = form.cleaned_data['prazo'],
                    data_ini = form.cleaned_data['data_ini'],
                    data_real = form.cleaned_data['data_real'],
                    data_fim = form.cleaned_data['data_fim'],
                    data_finalizacao = form.cleaned_data['data_finalizacao'],
                    data_finalizacao_sat = form.cleaned_data['data_finalizacao_sat'],
                    pendente_por = form.cleaned_data['pendente_por'],
                    status_pendencia = form.cleaned_data['status_pendencia'],
                    historico = form.cleaned_data['historico'],
                    id_departamento = form.cleaned_data['id_departamento'],
                    responsavel = form.cleaned_data['responsavel'],
                    autoridade = form.cleaned_data['autoridade'],
                    #dpto_correto = form.cleaned_data['dpto_correto'],
                    processo_relacionado = form.cleaned_data['processo_relacionado'],
                    id_pessoa = form.cleaned_data['id_pessoa'],
                    last_update = datetime.now(),
                    id_update = form.cleaned_data['id_update'],
                    #predecessor_1 = form.cleaned_data['predecessor_1'],
                    #predecessor_2 = form.cleaned_data['predecessor_2'],
                    #predecessor_3 = form.cleaned_data['predecessor_3'],
                    #anexo1 = form.cleaned_data['anexo1'],
                    #anexo2 = form.cleaned_data['anexo2'],
                    #anexo3 = form.cleaned_data['anexo3'],
                    #anexo4 = form.cleaned_data['anexo4'],
                    checado = form.cleaned_data['checado'],
                    etapa = form.cleaned_data['etapa'],
                    subetapa = form.cleaned_data['subetapa'],
                    retrospec = form.cleaned_data['retrospec'],
                    calendario = calendario,
                    data_calendario = data_calendario,
                    id_medicao = form.cleaned_data['id_medicao'],
                )
                tarefa.save()

                # Executores #
                if executores_form.is_valid():
                    new_executores = Executor(
                        executor1 = executores_form.cleaned_data['executor1'],
                        porcento1 = executores_form.cleaned_data['porcento1'],
                        executor2 = executores_form.cleaned_data['executor2'],
                        porcento2 = executores_form.cleaned_data['porcento2'],
                        executor3 = executores_form.cleaned_data['executor3'],
                        porcento3 = executores_form.cleaned_data['porcento3'],
                        executor4 = executores_form.cleaned_data['executor4'],
                        porcento4 = executores_form.cleaned_data['porcento4'],
                        executor5 = executores_form.cleaned_data['executor5'],
                        porcento5 = executores_form.cleaned_data['porcento5'],
                        executor6 = executores_form.cleaned_data['executor6'],
                        porcento6 = executores_form.cleaned_data['porcento6'],
                        executor7 = executores_form.cleaned_data['executor7'],
                        porcento7 = executores_form.cleaned_data['porcento7'],
                        executor8 = executores_form.cleaned_data['executor8'],
                        porcento8 = executores_form.cleaned_data['porcento8'],
                        executor9 = executores_form.cleaned_data['executor9'],
                        porcento9 = executores_form.cleaned_data['porcento9'],
                        executor10 = executores_form.cleaned_data['executor10'],
                        porcento10 = executores_form.cleaned_data['porcento10'],
                        id_tarefa = Tarefa.objects.get(pk=tarefa.id_tarefa),
                    )

                    new_executores.save()
                else:
                    context = {
                        'form' : form,
                        'executores_form' : executores_form,
                        'usuario' : usuario
                    }

            if (retrospectiva == ""):
                if (request.POST['classificacao'] != ""):
                    id_tarefa = Tarefa.objects.get(pk = tarefa.id_tarefa)
                    descricao = request.POST['classificacao']
                    stats = request.POST['rStat']
                    rResponsavel = request.POST['id_responsavel']

                    id_pessoa_objects = Pessoa.objects.all().filter(id_user=request.user.id)
                    id_update = id_pessoa_objects[0]
                    id_pessoa_objects = Pessoa.objects.all().filter(id_pessoa=rResponsavel)
                    rResponsavel = id_pessoa_objects[0]
                    nome_responsavel = id_pessoa_objects[0].nome
                    last_update = datetime.now()

                    retrospectiva = Retrospectiva(id_tarefa=id_tarefa, descricao=descricao, stats=stats, finalizado=0, id_update=id_update, last_update=last_update, id_responsavel=rResponsavel, nome_responsavel=nome_responsavel)
                    retrospectiva.save()
                    # print("Retrospectiva cadastrada!")
                else:
                    print("Não há retrospectiva!")
            else:
                retrospectiva = get_object_or_404(Retrospectiva, id_tarefa=id)
                retrospectiva.id_tarefa = Tarefa.objects.get(pk = tarefa.id_tarefa)
                retrospectiva.descricao = request.POST['classificacao']
                retrospectiva.stats = request.POST['rStat']
                retrospectiva.finalizado = request.POST['finalizado']
                rResponsavel = request.POST['id_responsavel']
                
                id_pessoa_objects = Pessoa.objects.all().filter(id_pessoa=rResponsavel)
                rResponsavel = id_pessoa_objects[0]
                retrospectiva.id_responsavel = rResponsavel
                retrospectiva.nome_responsavel = id_pessoa_objects[0].nome
                
                retrospectiva.save()

            if (r5w2h == ""):
                if (request.POST['rWhat'] != ""):
                    id_tarefa = Tarefa.objects.get(pk = tarefa.id_tarefa)
                    rWhat = request.POST['rWhat']
                    rWhy = request.POST['rWhy']
                    rWhere = request.POST['rWhere']
                    rWhen = request.POST['rWhen']
                    rWho = request.POST['rWho']
                    rHow = request.POST['rHow']
                    rHowMuch = request.POST['rHowMuch']

                    id_pessoa_objects = Pessoa.objects.all().filter(id_user=request.user.id)
                    id_update = id_pessoa_objects[0]
                    last_update = datetime.now()

                    r5w2h = R5w2h(id_tarefa=id_tarefa, rWhat=rWhat, rWhy=rWhy, rWhere=rWhere, rWhen=rWhen, rWho=rWho, rHow=rHow, rHowMuch=rHowMuch, id_update=id_update, last_update=last_update)
                    r5w2h.save()
                    # print("5w2h cadastrado!")
                else:
                    print("Não há 5w2h!")
            else:
                r5w2h = get_object_or_404(R5w2h, id_tarefa=id)
                r5w2h.id_tarefa = Tarefa.objects.get(pk = tarefa.id_tarefa)
                r5w2h.rWhat = request.POST['rWhat']
                r5w2h.rWhy = request.POST['rWhy']
                r5w2h.rWhere = request.POST['rWhere']
                r5w2h.rWhen = request.POST['rWhen']
                r5w2h.rWho = request.POST['rWho']
                r5w2h.rHow = request.POST['rHow']
                r5w2h.rHowMuch = request.POST['rHowMuch']
                
                r5w2h.save()
                # print("r5w2h atualizado!")

            if (solicitacao == ""):
                if (request.POST['proprietario_nome'] != ""):
                    id_tarefa = Tarefa.objects.get(pk = tarefa.id_tarefa)
                    empreendimento = request.POST['empreendimento']
                    bloco = request.POST['bloco']
                    unidade = request.POST['unidade']
                    proprietario_nome = request.POST['proprietario_nome']
                    proprietario_cpf = request.POST['proprietario_cpf']
                    proprietario_rg = request.POST['proprietario_rg']
                    proprietario_email = request.POST['proprietario_email']
                    solicitante_nome = request.POST['solicitante_nome']
                    solicitante_cpf = request.POST['solicitante_cpf']
                    solicitante_rg = request.POST['solicitante_rg']
                    solicitante_email = request.POST['solicitante_email']
                    telefone1 = request.POST['telefone1']
                    telefone2 = request.POST['telefone2']
                    status_processo = request.POST['status_processo']
                    aux = request.POST['data_finalizacao_sat']
                    data_finalizacao_sat = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                    aux = request.POST['data_entrega']
                    data_entrega = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                    tipo_solicitacao = request.POST['tipo_solicitacao']
                    tempo_total = request.POST['tempo_total']
                    satisfacao_avaliacao = request.POST['satisfacao_avaliacao']

                    solicitacao = Solicitacao(id_tarefa=id_tarefa, empreendimento=empreendimento, bloco=bloco, unidade=unidade, proprietario_nome=proprietario_nome, proprietario_cpf=proprietario_cpf, proprietario_rg=proprietario_rg, proprietario_email=proprietario_email, 
                    solicitante_nome=solicitante_nome, solicitante_cpf=solicitante_cpf, solicitante_rg=solicitante_rg, solicitante_email=solicitante_email, telefone1=telefone1, telefone2=telefone2, status_processo=status_processo, data_finalizacao_sat=data_finalizacao_sat, 
                    data_entrega=data_entrega, tipo_solicitacao=tipo_solicitacao, tempo_total=tempo_total, satisfacao_avaliacao=satisfacao_avaliacao
                    )
                    solicitacao.save()

                    try:
                        print("ambiente1: {}".format(request.POST['ambiente1']))
                        for j in range(int(request.POST['qtdProblemas'])):
                            id_solicitacao = solicitacao

                            ambiente = request.POST['ambiente'+ str(j + 1)]
                            descricao_sat = request.POST['descricao_sat'+ str(j + 1)]
                            tipo_reparo = request.POST['tipo_reparo'+ str(j + 1)]
                            historico_sat = request.POST['historico_sat'+ str(j + 1)]
                            procedencia = request.POST['procedencia'+ str(j + 1)]
                            estimativa_custo = request.POST['estimativa_custo'+ str(j + 1)]
                            material = request.POST['material'+ str(j + 1)]
                            duracao = request.POST['duracao'+ str(j + 1)]
                            raiz = request.POST['raiz'+ str(j + 1)]
                            try:
                                finalizado = request.POST['finalizado'+ str(j + 1)]
                                finalizado = 1
                            except:
                                finalizado = 0

                            problema = Problema(id_solicitacao=id_solicitacao, ambiente=ambiente, descricao_sat=descricao_sat, tipo_reparo=tipo_reparo, historico_sat=historico_sat, procedencia=procedencia, 
                            estimativa_custo=estimativa_custo, material=material, duracao=duracao, finalizado=finalizado, raiz=raiz)
                            problema.save()
                    except:
                        problema = Problema(id_solicitacao=solicitacao)
                        problema.save()
                else:
                    print("Não há solicitação/problema")
            else:
                solicitacao = get_object_or_404(Solicitacao, id_tarefa=id)
                solicitacao.id_tarefa = Tarefa.objects.get(pk = tarefa.id_tarefa)
                solicitacao.empreendimento = request.POST['empreendimento']
                solicitacao.bloco = request.POST['bloco']
                solicitacao.unidade = request.POST['unidade']
                solicitacao.proprietario_nome = request.POST['proprietario_nome']
                solicitacao.proprietario_cpf = request.POST['proprietario_cpf']
                solicitacao.proprietario_rg = request.POST['proprietario_rg']
                solicitacao.proprietario_email = request.POST['proprietario_email']
                solicitacao.solicitante_nome = request.POST['solicitante_nome']
                solicitacao.solicitante_cpf = request.POST['solicitante_cpf']
                solicitacao.solicitante_rg = request.POST['solicitante_rg']
                solicitacao.solicitante_email = request.POST['solicitante_email']
                solicitacao.telefone1 = request.POST['telefone1']
                solicitacao.telefone2 = request.POST['telefone2']
                solicitacao.status_processo = request.POST['status_processo']
                aux = request.POST['data_finalizacao_sat']
                solicitacao.data_finalizacao_sat = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                aux = request.POST['data_entrega']
                solicitacao.data_entrega = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                solicitacao.tipo_solicitacao = request.POST['tipo_solicitacao']
                solicitacao.tempo_total = request.POST['tempo_total']
                solicitacao.satisfacao_avaliacao = request.POST['satisfacao_avaliacao']

                solicitacao.save()

            if (medicao_terceiros == ""):
                if (request.POST['mes'] != '0'):
                    id_tarefa = request.POST['id_tarefa']
                    mes = request.POST['mes']
                    valor_bruto = request.POST['valor_bruto']
                    valor_liquido = request.POST['valor_liquido']
                    permuta = request.POST['permuta']

                    medicao_terceiros = MedicaoTerceiros(id_tarefa=id_tarefa, mes=mes, valor_bruto=valor_bruto, valor_liquido=valor_liquido, permuta=permuta)
                    medicao_terceiros.save()
                else:
                    print("Não há medição de terceiros")
            else:
                medicao_terceiros = get_object_or_404(MedicaoTerceiros, id_tarefa=request.POST['id_tarefa'])
                medicao_terceiros.id_tarefa = request.POST['id_tarefa']
                medicao_terceiros.mes = request.POST['mes']
                medicao_terceiros.valor_bruto = request.POST['valor_bruto']
                medicao_terceiros.valor_liquido = request.POST['valor_liquido']
                medicao_terceiros.permuta = request.POST['permuta']

                medicao_terceiros.save()

            if (juridico == ""):
                if (request.POST['id_resumo_processo'] != ""):
                    id_tarefa = id_juridico
                    escritorio = request.POST['escritorio']
                    escritorio_advogado = request.POST['escritorio_advogado']
                    resumo_processo = request.POST['id_resumo_processo']
                    numero_processo = request.POST['numero_processo']
                    if request.POST['prazo_interno'] != '':
                        aux = request.POST['prazo_interno']
                        prazo_interno = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                    else:
                        prazo_interno = None
                    observacoes = request.POST['id_observacoes']
                    valor_estimado = request.POST['valor_estimado']
                    valor_causa = request.POST['valor_causa']
                    valor_acordo = request.POST['valor_acordo']
                    autor_assistente = request.POST['autor_assistente']
                    autor_advogado = request.POST['autor_advogado']
                    reu_assistente = request.POST['reu_assistente']
                    reu_advogado = request.POST['reu_advogado']
                    perito = request.POST['perito']
                    preposto = request.POST['preposto']
                    jUnidade = request.POST['jUnidade']
                    jBloco = request.POST['jBloco']

                    juridico = Juridico(
                        id_tarefa=id_tarefa,
                        autor_assistente=autor_assistente,
                        autor_advogado=autor_advogado,
                        reu_assistente=reu_assistente,
                        reu_advogado=reu_advogado,
                        escritorio=escritorio,
                        escritorio_advogado=escritorio_advogado,
                        resumo_processo=resumo_processo,
                        numero_processo=numero_processo,
                        prazo_interno=prazo_interno,
                        observacoes=observacoes,
                        valor_estimado=valor_estimado,
                        valor_causa=valor_causa,
                        valor_acordo=valor_acordo,
                        perito=perito,
                        jUnidade=jUnidade,
                        jBloco=jBloco
                    )
                    juridico.save()

                    testemunha1 = request.POST['testemunha1']
                    if request.POST['testemunha2']:
                        testemunha2 = request.POST['testemunha2']
                    else:
                        testemunha2 = None
                    if request.POST['testemunha3']:
                        testemunha3 = request.POST['testemunha3']
                    else:
                        testemunha3 = None
                    if request.POST['testemunha4']:
                        testemunha4 = request.POST['testemunha4']
                    else:
                        testemunha4 = None
                    if request.POST['testemunha5']:
                        testemunha5 = request.POST['testemunha5']
                    else:
                        testemunha5 = None
                    if request.POST['testemunha6']:
                        testemunha6 = request.POST['testemunha6']
                    else:
                        testemunha6 = None
                    if request.POST['testemunha7']:
                        testemunha7 = request.POST['testemunha7']
                    else:
                        testemunha7 = None
                    if request.POST['testemunha8']:
                        testemunha8 = request.POST['testemunha8']
                    else:
                        testemunha8 = None
                    if request.POST['testemunha9']:
                        testemunha9 = request.POST['testemunha9']
                    else:
                        testemunha9 = None
                    if request.POST['testemunha10']:
                        testemunha10 = request.POST['testemunha10']
                    else:
                        testemunha10 = None

                    testemunhas = Testemunhas(
                        id_tarefa=id_tarefa,
                        testemunha1=testemunha1,
                        testemunha2=testemunha2,
                        testemunha3=testemunha3,
                        testemunha4=testemunha4,
                        testemunha5=testemunha5,
                        testemunha6=testemunha6,
                        testemunha7=testemunha7,
                        testemunha8=testemunha8,
                        testemunha9=testemunha9,
                        testemunha10=testemunha10
                    )
                    testemunhas.save()

                    autor1 = request.POST['autor1']
                    if request.POST['autor2']:
                        autor2 = request.POST['autor2']
                    else:
                        autor2 = None
                    if request.POST['autor3']:
                        autor3 = request.POST['autor3']
                    else:
                        autor3 = None
                    if request.POST['autor4']:
                        autor4 = request.POST['autor4']
                    else:
                        autor4 = None
                    if request.POST['autor5']:
                        autor5 = request.POST['autor5']
                    else:
                        autor5 = None
                    if request.POST['autor6']:
                        autor6 = request.POST['autor6']
                    else:
                        autor6 = None
                    if request.POST['autor7']:
                        autor7 = request.POST['autor7']
                    else:
                        autor7 = None
                    if request.POST['autor8']:
                        autor8 = request.POST['autor8']
                    else:
                        autor8 = None
                    if request.POST['autor9']:
                        autor9 = request.POST['autor9']
                    else:
                        autor9 = None
                    if request.POST['autor10']:
                        autor10 = request.POST['autor10']
                    else:
                        autor10 = None

                    autor = Autor(
                        id_tarefa=id_tarefa,
                        autor1=autor1,
                        autor2=autor2,
                        autor3=autor3,
                        autor4=autor4,
                        autor5=autor5,
                        autor6=autor6,
                        autor7=autor7,
                        autor8=autor8,
                        autor9=autor9,
                        autor10=autor10
                    )
                    autor.save()

                    reu1 = request.POST['reu1']
                    if request.POST['reu2']:
                        reu2 = request.POST['reu2']
                    else:
                        reu2 = None
                    if request.POST['reu3']:
                        reu3 = request.POST['reu3']
                    else:
                        reu3 = None
                    if request.POST['reu4']:
                        reu4 = request.POST['reu4']
                    else:
                        reu4 = None
                    if request.POST['reu5']:
                        reu5 = request.POST['reu5']
                    else:
                        reu5 = None
                    if request.POST['reu6']:
                        reu6 = request.POST['reu6']
                    else:
                        reu6 = None
                    if request.POST['reu7']:
                        reu7 = request.POST['reu7']
                    else:
                        reu7 = None
                    if request.POST['reu8']:
                        reu8 = request.POST['reu8']
                    else:
                        reu8 = None
                    if request.POST['reu9']:
                        reu9 = request.POST['reu9']
                    else:
                        reu9 = None
                    if request.POST['reu10']:
                        reu10 = request.POST['reu10']
                    else:
                        reu10 = None

                    reu = Reu(
                        id_tarefa=id_tarefa,
                        reu1=reu1,
                        reu2=reu2,
                        reu3=reu3,
                        reu4=reu4,
                        reu5=reu5,
                        reu6=reu6,
                        reu7=reu7,
                        reu8=reu8,
                        reu9=reu9,
                        reu10=reu10
                    )
                    reu.save()
                else:
                    print("Não há jurídico")
            else:
                juridico.escritorio = request.POST['escritorio']
                juridico.escritorio_advogado = request.POST['escritorio_advogado']
                juridico.resumo_processo = request.POST['id_resumo_processo']
                juridico.numero_processo = request.POST['numero_processo']
                juridico.autor_assistente = request.POST['autor_assistente']
                juridico.autor_advogado = request.POST['autor_advogado']
                juridico.reu_assistente = request.POST['reu_assistente']
                juridico.reu_advogado = request.POST['reu_advogado']
                aux = request.POST['prazo_interno']
                juridico.prazo_interno = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                juridico.observacoes = request.POST['id_observacoes']
                juridico.valor_estimado = request.POST['valor_estimado']
                juridico.valor_causa = request.POST['valor_causa']
                juridico.valor_acordo = request.POST['valor_acordo']
                juridico.perito = request.POST['perito']
                juridico.preposto = request.POST['preposto']
                juridico.jBloco = request.POST['jBloco']
                juridico.jUnidade = request.POST['jUnidade']

                juridico.save()

                testemunhas.testemunha1 = request.POST['testemunha1']
                if request.POST['testemunha2']:
                    testemunhas.testemunha2 = request.POST['testemunha2']
                else:
                    testemunhas.testemunha2 = None
                if request.POST['testemunha3']:
                    testemunhas.testemunha3 = request.POST['testemunha3']
                else:
                    testemunhas.testemunha3 = None
                if request.POST['testemunha4']:
                    testemunhas.testemunha4 = request.POST['testemunha4']
                else:
                    testemunhas.testemunha4 = None
                if request.POST['testemunha5']:
                    testemunhas.testemunha5 = request.POST['testemunha5']
                else:
                    testemunhas.testemunha5 = None
                if request.POST['testemunha6']:
                    testemunhas.testemunha6 = request.POST['testemunha6']
                else:
                    testemunhas.testemunha6 = None
                if request.POST['testemunha7']:
                    testemunhas.testemunha7 = request.POST['testemunha7']
                else:
                    testemunhas.testemunha7 = None
                if request.POST['testemunha8']:
                    testemunhas.testemunha8 = request.POST['testemunha8']
                else:
                    testemunhas.testemunha8 = None
                if request.POST['testemunha9']:
                    testemunhas.testemunha9 = request.POST['testemunha9']
                else:
                    testemunhas.testemunha9 = None
                if request.POST['testemunha10']:
                    testemunhas.testemunha10 = request.POST['testemunha10']
                else:
                    testemunhas.testemunha10 = None
                testemunhas.save()

                autor.autor1 = request.POST['autor1']
                if request.POST['autor2']:
                    autor.autor2 = request.POST['autor2']
                else:
                    autor.autor2 = None
                if request.POST['autor3']:
                    autor.autor3 = request.POST['autor3']
                else:
                    autor.autor3 = None
                if request.POST['autor4']:
                    autor.autor4 = request.POST['autor4']
                else:
                    autor.autor4 = None
                if request.POST['autor5']:
                    autor.autor5 = request.POST['autor5']
                else:
                    autor.autor5 = None
                if request.POST['autor6']:
                    autor.autor6 = request.POST['autor6']
                else:
                    autor.autor6 = None
                if request.POST['autor7']:
                    autor.autor7 = request.POST['autor7']
                else:
                    autor.autor7 = None
                if request.POST['autor8']:
                    autor.autor8 = request.POST['autor8']
                else:
                    autor.autor8 = None
                if request.POST['autor9']:
                    autor.autor9 = request.POST['autor9']
                else:
                    autor.autor9 = None
                if request.POST['autor10']:
                    autor.autor10 = request.POST['autor10']
                else:
                    autor.autor10 = None
                autor.save()

                reu.reu1 = request.POST['reu1']
                if request.POST['reu2']:
                    reu.reu2 = request.POST['reu2']
                else:
                    reu.reu2 = None
                if request.POST['reu3']:
                    reu.reu3 = request.POST['reu3']
                else:
                    reu.reu3 = None
                if request.POST['reu4']:
                    reu.reu4 = request.POST['reu4']
                else:
                    reu.reu4 = None
                if request.POST['reu5']:
                    reu.reu5 = request.POST['reu5']
                else:
                    reu.reu5 = None
                if request.POST['reu6']:
                    reu.reu6 = request.POST['reu6']
                else:
                    reu.reu6 = None
                if request.POST['reu7']:
                    reu.reu7 = request.POST['reu7']
                else:
                    reu.reu7 = None
                if request.POST['reu8']:
                    reu.reu8 = request.POST['reu8']
                else:
                    reu.reu8 = None
                if request.POST['reu9']:
                    reu.reu9 = request.POST['reu9']
                else:
                    reu.reu9 = None
                if request.POST['reu10']:
                    reu.reu10 = request.POST['reu10']
                else:
                    reu.reu10 = None
                reu.save()

            messages.success(request, 'A tarefa foi cadastrada com sucesso!', extra_tags='success')
            return HttpResponseRedirect(reverse('Tarefa:editar', args=(tarefa.id_tarefa,)))
        else:
            context = {
                'form' : form,
                'executores_form' : executores_form,
                'usuario' : usuario
            }
            messages.success(request, 'Falha ao cadastrar a tarefa!', extra_tags='danger')
            return render(request, 'cadastrarTarefas.html', context)

    form = TarefaForms(request)
    executores_form = ExecutorForms(request)


    context = {
        'form' : form,
        'usuario' : usuario,
        'executores_form' : executores_form,
        "r5w2h" : r5w2h,
        "retrospectiva" : retrospectiva,
        "solicitacao" : solicitacao,
        "medicao_terceiros" : medicao_terceiros,
        "medicao_terceiros_form" : medicao_terceiros_form,
        "locacao" : locacao,
        "solicitacao_form" : solicitacao_form,
        "locacao_form" : locacao_form,
        "juridico_form" : juridico_form,
        "testemunhas_form" : testemunhas_form,
        "autor_form" : autor_form,
        "reu_form" : reu_form,
        "problema" : problema
    }

    return render(request, 'cadastrarTarefas.html', context)

@login_required(login_url=urls.getUrlSubdominio())
def duplicarTarefas(request, id):
    usuario = get_user(request.user)

    if request.method == 'POST':
        form = TarefaForms(request, request.POST)
        executores_form = ExecutorForms(request, request.POST)

        calendario = None
        data_calendario = None

        if request.POST['calendario'] == '1':
            calendario = 1
            data_calendario = "{}-00:00".format(request.POST['data_calendario'])

        # Tarefas #
        if form.is_valid():
            new_tarefa = Tarefa(
                id_empresa = usuario.id_empresa,
                descri = form.cleaned_data['descri'],
                id_centro_custo = form.cleaned_data['id_centro_custo'],
                prioridade = form.cleaned_data['prioridade'],
                stat = form.cleaned_data['stat'],
                id_tamanho = form.cleaned_data['id_tamanho'],
                porcentagem = form.cleaned_data['porcentagem'],
                prazo = form.cleaned_data['prazo'],
                data_ini = form.cleaned_data['data_ini'],
                data_real = form.cleaned_data['data_real'],
                data_fim = form.cleaned_data['data_fim'],
                data_finalizacao = form.cleaned_data['data_finalizacao'],
                data_finalizacao_sat = form.cleaned_data['data_finalizacao_sat'],
                pendente_por = form.cleaned_data['pendente_por'],
                status_pendencia = form.cleaned_data['status_pendencia'],
                historico = form.cleaned_data['historico'],
                id_departamento = form.cleaned_data['id_departamento'],
                responsavel = form.cleaned_data['responsavel'],
                autoridade = form.cleaned_data['autoridade'],
                processo_relacionado = form.cleaned_data['processo_relacionado'],
                id_pessoa = form.cleaned_data['id_pessoa'],
                last_update = datetime.now(),
                id_update = form.cleaned_data['id_update'],
                checado = form.cleaned_data['checado'],
                etapa = form.cleaned_data['etapa'],
                subetapa = form.cleaned_data['subetapa'],
                retrospec = form.cleaned_data['retrospec'],
                calendario = calendario,
                data_calendario = data_calendario,
            )
            new_tarefa.save()

            # Executores #
            if executores_form.is_valid():
                new_executores = Executor(
                    executor1 = executores_form.cleaned_data['executor1'],
                    porcento1 = executores_form.cleaned_data['porcento1'],
                    executor2 = executores_form.cleaned_data['executor2'],
                    porcento2 = executores_form.cleaned_data['porcento2'],
                    executor3 = executores_form.cleaned_data['executor3'],
                    porcento3 = executores_form.cleaned_data['porcento3'],
                    executor4 = executores_form.cleaned_data['executor4'],
                    porcento4 = executores_form.cleaned_data['porcento4'],
                    executor5 = executores_form.cleaned_data['executor5'],
                    porcento5 = executores_form.cleaned_data['porcento5'],
                    executor6 = executores_form.cleaned_data['executor6'],
                    porcento6 = executores_form.cleaned_data['porcento6'],
                    executor7 = executores_form.cleaned_data['executor7'],
                    porcento7 = executores_form.cleaned_data['porcento7'],
                    executor8 = executores_form.cleaned_data['executor8'],
                    porcento8 = executores_form.cleaned_data['porcento8'],
                    executor9 = executores_form.cleaned_data['executor9'],
                    porcento9 = executores_form.cleaned_data['porcento9'],
                    executor10 = executores_form.cleaned_data['executor10'],
                    porcento10 = executores_form.cleaned_data['porcento10'],
                    id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                )

                new_executores.save()

                messages.success(request, 'A tarefa foi duplicada com sucesso!', extra_tags='success')
                return HttpResponseRedirect(reverse('Tarefa:editar', args=(new_tarefa.id_tarefa,)))

            else:
                context = {
                    'form' : form,
                    'executores_form' : executores_form,
                    'usuario' : usuario
                }
                messages.success(request, 'Falha ao cadastrar a tarefa!', extra_tags='danger')
                return HttpResponseRedirect(reverse('Tarefa:duplicar', args=(id,)))
        else:
            context = {
                'form' : form,
                'executores_form' : executores_form,
                'usuario' : usuario
            }
            messages.success(request, 'Falha ao cadastrar a tarefa!', extra_tags='danger')
            return HttpResponseRedirect(reverse('Tarefa:duplicar', args=(id,)))

    tarefa = get_object_or_404(Tarefa, pk=id, id_empresa=usuario.id_empresa)

    if tarefa.data_calendario != None:
        tarefa.data_calendario = tarefa.data_calendario.strftime('%d/%m/%Y, %H:%M:%S')

    executores = get_object_or_404(Executor, id_tarefa=id)

    form = TarefaForms(request, instance=tarefa)
    executores_form = ExecutorForms(request, instance=executores)

    context = {
        "form" : form,
        "tarefa" : tarefa,
        "usuario" : usuario,
        "executores_form": executores_form,
    }

    return render(request, 'duplicarTarefas.html', context)

@login_required(login_url=urls.getUrlSubdominio())
def editarTarefas(request, id):
    usuario = get_user(request.user)

    etapas = Etapas.objects.filter(id_empresa=usuario.id_empresa)
    subetapas = SubEtapas.objects.filter(id_empresa=usuario.id_empresa)

    tarefa = get_object_or_404(Tarefa, pk=id, id_empresa=usuario.id_empresa)
    if tarefa.data_calendario != None:
        tarefa.data_calendario = tarefa.data_calendario.strftime('%d/%m/%Y, %H:%M:%S')
    # Verifica o status da tarefa ao carregar a página para uso em tarefas de locação
    statusLocacao = tarefa.stat
    id_stats = tarefa.id_status
    executores = get_object_or_404(Executor, id_tarefa=id)
    
    try:
        retrospectiva = get_object_or_404(Retrospectiva, id_tarefa=id)
    except:
        retrospectiva = ""

    try:
        r5w2h = get_object_or_404(R5w2h, id_tarefa=id)
    except:
        r5w2h = ""

    try:
        solicitacao = get_object_or_404(Solicitacao, id_tarefa=id)
        problema = Problema.objects.filter(id_solicitacao=solicitacao.id_solicitacao).exclude(ambiente=None)
        if len(problema) == 0:
            problema = ""
    except:
        solicitacao = ""
        problema = ""
        
    try:
        medicao_terceiros = get_object_or_404(MedicaoTerceiros, id_tarefa=id)
    except:
        medicao_terceiros = ""
    
    try:
        locacao = get_object_or_404(Locacao, id_tarefa=tarefa.id_locacao)
    except:
        locacao = ""

    try:
        if locacao.id_tarefa != None and tarefa.id_status != 11:
            try:
                filhos = Tarefa.objects.filter(id_locacao=tarefa.id_tarefa).order_by('id_status')
                executoresFilhos = FluxoLocacao.objects.filter(id_locacao=tarefa.id_tarefa).order_by('id_status')
                filhaStat = []
                for filho in filhos:
                    filhaStat.append(filho.stat)
                    filho.data_ini = filho.data_ini.strftime('%d/%m/%Y')
                    filho.data_fim = filho.data_fim.strftime('%d/%m/%Y')
            except:
                filhos = ""
                executoresFilhos = ""
        else:
            filhos = ""
            executoresFilhos = ""
    except:
        filhos = ""
        executoresFilhos = ""

    try:
        filhosTarefa = TarefasKanban.objects.filter(id_filho=tarefa.id_tarefa)

        filhosAFazer = []
        filhosFazendo = []
        filhosFeito = []

        for filho in filhosTarefa:
            filho.data_ini = filho.data_ini.strftime('%d/%m/%Y')
            filho.data_fim = filho.data_fim.strftime('%d/%m/%Y')
            filho.Executores = getExecutores(filho)
            if filho.stat == "A fazer" and filho.id_status == 1:
                filhosAFazer.append(filho)
            elif filho.stat == "Fazendo" and filho.id_status == 1:
                filhosFazendo.append(filho)
            elif filho.stat == "Feito" and filho.id_status == 1:
                filhosFeito.append(filho)
            else:
                None
    except:
        filhosTarefa = ""

    try:
        juridico = get_object_or_404(Juridico, id_tarefa=tarefa.id_juridico)
        testemunhas = get_object_or_404(Testemunhas, id_tarefa=tarefa.id_juridico)
        tarefas = Tarefa.objects.filter(id_juridico=tarefa.id_juridico)
    except:
        juridico = ""
        testemunhas = ""
        tarefas = ""


    try:
        autor = get_object_or_404(Autor, id_tarefa=tarefa.id_juridico)
        reu = get_object_or_404(Reu, id_tarefa=tarefa.id_juridico)
    except:
        autor = ""
        reu = ""

    form = TarefaForms(request, instance=tarefa)
    executores_form = ExecutorFormsEditar(request, instance=executores)

    try:
        solicitacao_form = SolicitacaoForms(request, instance=solicitacao)
    except:
        solicitacao_form = SolicitacaoForms(request)

    try:
        medicao_terceiros_form = EditarMedicaoTerceiros(instance=medicao_terceiros)
    except:
        medicao_terceiros_form = EditarMedicaoTerceiros()

    try:
        locacao_form = LocacaoForms(instance=locacao)
    except:
        locacao_form = LocacaoForms()

    try:
        juridico_form = JuridicoForms(request, instance=juridico)
        testemunhas_form = TestemunhasForms(instance=testemunhas)
    except:
        juridico_form = JuridicoForms(request)
        testemunhas_form = TestemunhasForms()

    try:
        autor_form = AutorForms(instance=autor)
        reu_form = ReuForms(instance=reu)
    except:
        autor_form = AutorForms()
        reu_form = ReuForms()

    if request.method == 'POST':
        # Tarefa # 

        # Buscando a instancia da tarefa e criando o form carregando os dados do POST
        tarefa = get_object_or_404(Tarefa, pk=request.POST['id_tarefa'])
        # tarefa.data_calendario = tarefa.data_calendario.strftime('%d/%m/%Y, %H:%M:%S')
        FormTarefa = TarefaForms(request, request.POST, instance=tarefa)

        # Valida e salva
        if FormTarefa.is_valid():
            tarefa = FormTarefa.save(commit=False)

            tarefa.calendario = None
            tarefa.data_calendario = None

            if request.POST['calendario'] == '1':
                tarefa.calendario = 1
                tarefa.data_calendario = "{}-00:00".format(request.POST['data_calendario'])
                
            if request.POST['processo_relacionado'] == '63':
                if tarefa.id_status == 4 and tarefa.stat == "Feito" and statusLocacao != "Feito":
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)

                    # Busca dados da tarefa mãe
                    id_locacao = tarefa.id_locacao
                    tarefaMae = get_object_or_404(Tarefa, pk=id_locacao)
                    locacao_padrao_orcar = get_object_or_404(LocacaoEditar, id_locacao_editar=4)
                    locacao_padrao = get_object_or_404(LocacaoEditar, id_locacao_editar=5)
                    
                    descricao_ambiente = tarefa.descri.split(locacao_padrao_orcar.descricao)

                    # Nova tarefa # - Pagar
                    new_tarefa = Tarefa(
                        id_empresa = usuario.id_empresa,
                        descri = locacao_padrao.descricao + " - " + descricao_ambiente[1],
                        id_centro_custo = tarefa.id_centro_custo,
                        prioridade = tarefa.prioridade,
                        stat = "A fazer",
                        id_tamanho = locacao_padrao.id_tamanho,
                        porcentagem = 0,
                        prazo = locacao_padrao.prazo,
                        data_ini = tarefa.data_fim + timedelta(days = 3),
                        data_real = tarefa.data_fim + timedelta(days = 3),
                        # Acrescenta +3 dias a partir da finalização da anterior.
                        data_fim = tarefa.data_fim + timedelta(days = locacao_padrao.prazo),
                        data_finalizacao = tarefa.data_fim + timedelta(days = locacao_padrao.prazo),
                        data_finalizacao_sat = tarefa.data_finalizacao_sat,
                        status_pendencia = locacao_padrao.status_pendencia + " " + descricao_ambiente[1],
                        historico = "",
                        id_departamento = locacao_padrao.id_departamento,
                        responsavel = locacao_padrao.id_responsavel,
                        autoridade = locacao_padrao.id_autoridade,
                        processo_relacionado = tarefa.processo_relacionado,
                        id_pessoa = tarefa.id_pessoa,
                        last_update = datetime.now(),
                        id_update = tarefa.id_update,
                        checado = locacao_padrao.id_checado,
                        pendente_por = locacao_padrao.id_pendente_por,
                        etapa = tarefa.etapa,
                        subetapa = tarefa.subetapa,
                        retrospec = tarefa.retrospec,
                        id_locacao = id_locacao,
                        id_status = 5,
                    )
                    new_tarefa.save()

                    # Executores #
                    new_executores = Executor(
                        executor1 = locacao_padrao.id_executor1,
                        porcento1 = locacao_padrao.porcento1,
                        executor2 = locacao_padrao.id_executor2,
                        porcento2 = locacao_padrao.porcento2,
                        executor3 = locacao_padrao.id_executor3,
                        porcento3 = locacao_padrao.porcento3,
                        executor4 = locacao_padrao.id_executor4,
                        porcento4 = locacao_padrao.porcento4,
                        executor5 = locacao_padrao.id_executor5,
                        porcento5 = locacao_padrao.porcento5,
                        executor6 = locacao_padrao.id_executor6,
                        porcento6 = locacao_padrao.porcento6,
                        executor7 = locacao_padrao.id_executor7,
                        porcento7 = locacao_padrao.porcento7,
                        executor8 = locacao_padrao.id_executor8,
                        porcento8 = locacao_padrao.porcento8,
                        executor9 = locacao_padrao.id_executor9,
                        porcento9 = locacao_padrao.porcento9,
                        executor10 = locacao_padrao.id_executor10,
                        porcento10 = locacao_padrao.porcento10,
                        id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                    )
                    new_executores.save()

                    # Nova tarefa # - Instalar
                    locacao_padrao = get_object_or_404(LocacaoEditar, id_locacao_editar=6)
                    new_tarefa = Tarefa(
                        id_empresa = usuario.id_empresa,
                        descri = locacao_padrao.descricao + " " + descricao_ambiente[1],
                        id_centro_custo = tarefa.id_centro_custo,
                        prioridade = tarefa.prioridade,
                        stat = "A fazer",
                        id_tamanho = locacao_padrao.id_tamanho,
                        porcentagem = 0,
                        prazo = locacao_padrao.prazo,
                        data_ini = tarefa.data_fim + timedelta(days = 5),
                        data_real = tarefa.data_fim + timedelta(days = 5),
                        # Acrescenta +3 dias a partir da finalização da anterior.
                        data_fim = tarefa.data_fim + timedelta(days = 5) + timedelta(days = locacao_padrao.prazo),
                        data_finalizacao = tarefa.data_finalizacao,
                        data_finalizacao_sat = tarefa.data_finalizacao_sat,
                        status_pendencia = locacao_padrao.status_pendencia + " " + descricao_ambiente[1],
                        historico = "",
                        id_departamento = locacao_padrao.id_departamento,
                        responsavel = locacao_padrao.id_responsavel,
                        autoridade = locacao_padrao.id_autoridade,
                        processo_relacionado = tarefa.processo_relacionado,
                        id_pessoa = tarefa.id_pessoa,
                        last_update = datetime.now(),
                        id_update = tarefa.id_update,
                        checado = locacao_padrao.id_checado,
                        pendente_por = locacao_padrao.id_pendente_por,
                        etapa = tarefa.etapa,
                        subetapa = tarefa.subetapa,
                        retrospec = tarefa.retrospec,
                        id_locacao = id_locacao,
                        id_status = 6,
                    )
                    new_tarefa.save()

                    # Executores #
                    
                    if 'Móveis' in str(descricao_ambiente[1]):
                        new_executores = Executor(
                            executor1 = get_object_or_404(Pessoa, id_pessoa=82),
                            porcento1 = 100,
                            executor2 = get_object_or_404(Pessoa, id_pessoa=10),
                            porcento2 = 10,
                            executor3 = None,
                            porcento3 = None,
                            executor4 = None,
                            porcento4 = None,
                            executor5 = None,
                            porcento5 = None,
                            executor6 = None,
                            porcento6 = None,
                            executor7 = None,
                            porcento7 = None,
                            executor8 = None,
                            porcento8 = None,
                            executor9 = None,
                            porcento9 = None,
                            executor10 = None,
                            porcento10 = None,
                            id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                        )
                        new_executores.save()
                    elif 'Aquecedor' in str(descricao_ambiente[1]):
                        new_executores = Executor(
                            executor1 = get_object_or_404(Pessoa, id_pessoa=82),
                            porcento1 = 100,
                            executor2 = get_object_or_404(Pessoa, id_pessoa=10),
                            porcento2 = 10,
                            executor3 = None,
                            porcento3 = None,
                            executor4 = None,
                            porcento4 = None,
                            executor5 = None,
                            porcento5 = None,
                            executor6 = None,
                            porcento6 = None,
                            executor7 = None,
                            porcento7 = None,
                            executor8 = None,
                            porcento8 = None,
                            executor9 = None,
                            porcento9 = None,
                            executor10 = None,
                            porcento10 = None,
                            id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                        )
                        new_executores.save()
                    elif 'Luminárias' in str(descricao_ambiente[1]):
                        new_executores = Executor(
                            executor1 = get_object_or_404(Pessoa, id_pessoa=14),
                            porcento1 = 100,
                            executor2 = get_object_or_404(Pessoa, id_pessoa=269),
                            porcento2 = 100,
                            executor3 = None,
                            porcento3 = None,
                            executor4 = None,
                            porcento4 = None,
                            executor5 = None,
                            porcento5 = None,
                            executor6 = None,
                            porcento6 = None,
                            executor7 = None,
                            porcento7 = None,
                            executor8 = None,
                            porcento8 = None,
                            executor9 = None,
                            porcento9 = None,
                            executor10 = None,
                            porcento10 = None,
                            id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                        )
                        new_executores.save()
                    elif 'Box' in str(descricao_ambiente[1]):
                        new_executores = Executor(
                            executor1 = get_object_or_404(Pessoa, id_pessoa=14),
                            porcento1 = 100,
                            executor2 = get_object_or_404(Pessoa, id_pessoa=269),
                            porcento2 = 100,
                            executor3 = None,
                            porcento3 = None,
                            executor4 = None,
                            porcento4 = None,
                            executor5 = None,
                            porcento5 = None,
                            executor6 = None,
                            porcento6 = None,
                            executor7 = None,
                            porcento7 = None,
                            executor8 = None,
                            porcento8 = None,
                            executor9 = None,
                            porcento9 = None,
                            executor10 = None,
                            porcento10 = None,
                            id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                        )
                        new_executores.save()
                    elif 'Duchas' in str(descricao_ambiente[1]):
                        new_executores = Executor(
                            executor1 = get_object_or_404(Pessoa, id_pessoa=14),
                            porcento1 = 100,
                            executor2 = get_object_or_404(Pessoa, id_pessoa=269),
                            porcento2 = 100,
                            executor3 = None,
                            porcento3 = None,
                            executor4 = None,
                            porcento4 = None,
                            executor5 = None,
                            porcento5 = None,
                            executor6 = None,
                            porcento6 = None,
                            executor7 = None,
                            porcento7 = None,
                            executor8 = None,
                            porcento8 = None,
                            executor9 = None,
                            porcento9 = None,
                            executor10 = None,
                            porcento10 = None,
                            id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                        )
                        new_executores.save()
                    else:
                        new_executores = Executor(
                            executor1 = locacao_padrao.id_executor1,
                            porcento1 = locacao_padrao.porcento1,
                            executor2 = locacao_padrao.id_executor2,
                            porcento2 = locacao_padrao.porcento2,
                            executor3 = locacao_padrao.id_executor3,
                            porcento3 = locacao_padrao.porcento3,
                            executor4 = locacao_padrao.id_executor4,
                            porcento4 = locacao_padrao.porcento4,
                            executor5 = locacao_padrao.id_executor5,
                            porcento5 = locacao_padrao.porcento5,
                            executor6 = locacao_padrao.id_executor6,
                            porcento6 = locacao_padrao.porcento6,
                            executor7 = locacao_padrao.id_executor7,
                            porcento7 = locacao_padrao.porcento7,
                            executor8 = locacao_padrao.id_executor8,
                            porcento8 = locacao_padrao.porcento8,
                            executor9 = locacao_padrao.id_executor9,
                            porcento9 = locacao_padrao.porcento9,
                            executor10 = locacao_padrao.id_executor10,
                            porcento10 = locacao_padrao.porcento10,
                            id_tarefa = Tarefa.objects.get(pk=tarefa.id_tarefa),
                        )
                        new_executores.save()
                else:
                    tarefa = FormTarefa.save(commit=False)
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)

                if (locacao == ""):
                    if (request.POST['lBloco'] != "---"):
                        id_tarefa = tarefa.id_locacao
                        bloco = request.POST['lBloco']
                        unidade = request.POST['lUnidade']

                        locacao = Locacao(id_tarefa=id_tarefa, lBloco=bloco, lUnidade=unidade)
                        locacao.save()
                    else:
                        print("Não há locacao")
                else:
                    if (tarefa.id_locacao != None):
                        locacao = get_object_or_404(Locacao, id_tarefa=request.POST['id_locacao'])
                        locacao.id_tarefa = tarefa.id_locacao
                        locacao.lBloco = request.POST['lBloco']
                        locacao.lUnidade = request.POST['lUnidade']

                        tarefa.id_locacao = tarefa.id_locacao
                        tarefa.save()

                        locacao.save()

                tarefasFilhas = Tarefa.objects.filter(id_locacao=tarefa.id_locacao).order_by('id_status')
                qtdFeito = 0
                i = 0
                
                for filha in tarefasFilhas:
                    if filhos != "" and len(filhos) != 0:
                        if filha.id_tarefa != tarefa.id_tarefa:
                            filha.stat = request.POST['stat{}'.format(filha.id_tarefa)]
                            data_ini = request.POST['data_ini{}'.format(filha.id_tarefa)].split('/')
                            filha.data_ini = "{}-{}-{}".format(data_ini[2], data_ini[1], data_ini[0])
                            data_fim = request.POST['data_fim{}'.format(filha.id_tarefa)].split('/')
                            filha.data_fim = "{}-{}-{}".format(data_fim[2], data_fim[1], data_fim[0])
                            filha.id_tamanho = Tamanho.objects.get(id_tamanho = request.POST['tamanho{}'.format(filha.id_tarefa)])
                            filha.status_pendencia = request.POST['status_pendencia{}'.format(filha.id_tarefa)]

                            if filha.stat == "Feito":
                                filha.porcentagem = 100

                            filha.save()

                            if filha.id_status == 4 and request.POST['stat{}'.format(filha.id_tarefa)] == "Feito" and filhaStat[i] != "Feito":
                                locacao_padrao_orcar = get_object_or_404(LocacaoEditar, id_locacao_editar=4)
                                locacao_padrao = get_object_or_404(LocacaoEditar, id_locacao_editar=5)
                                
                                descricao_ambiente = filha.descri.split(locacao_padrao_orcar.descricao)
                                print("tarefa: {}\nfilho: {}".format(tarefa.data_fim, filha.data_fim))
                                aux = filha.data_fim.split("-")

                                # if int(aux[1]) != 0:
                                #     data_fim = datetime(int(aux[0]), int(aux[1]) - 1, int(aux[2]))
                                # else:
                                data_fim = datetime(int(aux[0]), int(aux[1]), int(aux[2]))
                                    
                                print(data_fim)
                                # Nova tarefa # - Pagar
                                new_tarefa = Tarefa(
                                    id_empresa = usuario.id_empresa,
                                    descri = locacao_padrao.descricao + " - " + descricao_ambiente[1],
                                    id_centro_custo = tarefa.id_centro_custo,
                                    prioridade = tarefa.prioridade,
                                    stat = "A fazer",
                                    id_tamanho = locacao_padrao.id_tamanho,
                                    porcentagem = 0,
                                    prazo = locacao_padrao.prazo,
                                    data_ini = data_fim + timedelta(days = 3),
                                    data_real = data_fim + timedelta(days = 3),
                                    # Acrescenta +3 dias a partir da finalização da anterior.
                                    data_fim = data_fim + timedelta(days = (3 + locacao_padrao.prazo)),
                                    data_finalizacao = data_fim + timedelta(days = (3 + locacao_padrao.prazo)),
                                    data_finalizacao_sat = tarefa.data_finalizacao_sat,
                                    status_pendencia = locacao_padrao.status_pendencia + " " + descricao_ambiente[1],
                                    historico = "",
                                    id_departamento = locacao_padrao.id_departamento,
                                    responsavel = locacao_padrao.id_responsavel,
                                    autoridade = locacao_padrao.id_autoridade,
                                    processo_relacionado = tarefa.processo_relacionado,
                                    id_pessoa = tarefa.id_pessoa,
                                    last_update = datetime.now(),
                                    id_update = tarefa.id_update,
                                    checado = locacao_padrao.id_checado,
                                    pendente_por = locacao_padrao.id_pendente_por,
                                    etapa = tarefa.etapa,
                                    subetapa = tarefa.subetapa,
                                    retrospec = tarefa.retrospec,
                                    id_locacao = tarefa.id_tarefa,
                                    id_status = 5,
                                )
                                new_tarefa.save()

                                # Executores #
                                new_executores = Executor(
                                    executor1 = locacao_padrao.id_executor1,
                                    porcento1 = locacao_padrao.porcento1,
                                    executor2 = locacao_padrao.id_executor2,
                                    porcento2 = locacao_padrao.porcento2,
                                    executor3 = locacao_padrao.id_executor3,
                                    porcento3 = locacao_padrao.porcento3,
                                    executor4 = locacao_padrao.id_executor4,
                                    porcento4 = locacao_padrao.porcento4,
                                    executor5 = locacao_padrao.id_executor5,
                                    porcento5 = locacao_padrao.porcento5,
                                    executor6 = locacao_padrao.id_executor6,
                                    porcento6 = locacao_padrao.porcento6,
                                    executor7 = locacao_padrao.id_executor7,
                                    porcento7 = locacao_padrao.porcento7,
                                    executor8 = locacao_padrao.id_executor8,
                                    porcento8 = locacao_padrao.porcento8,
                                    executor9 = locacao_padrao.id_executor9,
                                    porcento9 = locacao_padrao.porcento9,
                                    executor10 = locacao_padrao.id_executor10,
                                    porcento10 = locacao_padrao.porcento10,
                                    id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                                )
                                new_executores.save()

                                # Nova tarefa # - Instalar
                                locacao_padrao = get_object_or_404(LocacaoEditar, id_locacao_editar=6)
                                new_tarefa = Tarefa(
                                    id_empresa = usuario.id_empresa,
                                    descri = locacao_padrao.descricao + " " + descricao_ambiente[1],
                                    id_centro_custo = tarefa.id_centro_custo,
                                    prioridade = tarefa.prioridade,
                                    stat = "A fazer",
                                    id_tamanho = locacao_padrao.id_tamanho,
                                    porcentagem = 0,
                                    prazo = locacao_padrao.prazo,
                                    data_ini = data_fim + timedelta(days = 5),
                                    data_real = data_fim + timedelta(days = 5),
                                    # Acrescenta +3 dias a partir da finalização da anterior.
                                    data_fim = data_fim + timedelta(days = (5 + locacao_padrao.prazo)),
                                    data_finalizacao = data_fim + timedelta(days = (5 + locacao_padrao.prazo)),
                                    data_finalizacao_sat = tarefa.data_finalizacao_sat,
                                    status_pendencia = locacao_padrao.status_pendencia + " " + descricao_ambiente[1],
                                    historico = "",
                                    id_departamento = locacao_padrao.id_departamento,
                                    responsavel = locacao_padrao.id_responsavel,
                                    autoridade = locacao_padrao.id_autoridade,
                                    processo_relacionado = tarefa.processo_relacionado,
                                    id_pessoa = tarefa.id_pessoa,
                                    last_update = datetime.now(),
                                    id_update = tarefa.id_update,
                                    checado = locacao_padrao.id_checado,
                                    pendente_por = locacao_padrao.id_pendente_por,
                                    etapa = tarefa.etapa,
                                    subetapa = tarefa.subetapa,
                                    retrospec = tarefa.retrospec,
                                    id_locacao = tarefa.id_tarefa,
                                    id_status = 6,
                                )
                                new_tarefa.save()

                                # Executores #
                                new_executores = Executor(
                                    executor1 = locacao_padrao.id_executor1,
                                    porcento1 = locacao_padrao.porcento1,
                                    executor2 = locacao_padrao.id_executor2,
                                    porcento2 = locacao_padrao.porcento2,
                                    executor3 = locacao_padrao.id_executor3,
                                    porcento3 = locacao_padrao.porcento3,
                                    executor4 = locacao_padrao.id_executor4,
                                    porcento4 = locacao_padrao.porcento4,
                                    executor5 = locacao_padrao.id_executor5,
                                    porcento5 = locacao_padrao.porcento5,
                                    executor6 = locacao_padrao.id_executor6,
                                    porcento6 = locacao_padrao.porcento6,
                                    executor7 = locacao_padrao.id_executor7,
                                    porcento7 = locacao_padrao.porcento7,
                                    executor8 = locacao_padrao.id_executor8,
                                    porcento8 = locacao_padrao.porcento8,
                                    executor9 = locacao_padrao.id_executor9,
                                    porcento9 = locacao_padrao.porcento9,
                                    executor10 = locacao_padrao.id_executor10,
                                    porcento10 = locacao_padrao.porcento10,
                                    id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                                )
                                new_executores.save()
                        i += 1

                    if(filha.stat == "Feito"):
                        qtdFeito += 1
                
                tarefasFilhas = Tarefa.objects.filter(id_locacao=tarefa.id_locacao).order_by('id_status')
                qtdFeito = len(tarefasFilhas) - qtdFeito

                if(qtdFeito == 1):
                    tarefaMae = get_object_or_404(Tarefa, pk=tarefa.id_locacao)
                    tarefaMae.stat = "Feito"
                    tarefaMae.data_fim = date.today()
                    tarefaMae.historico = tarefaMae.status_pendencia + "\n" + tarefaMae.historico
                    tarefaMae.status_pendencia = ""
                    tarefaMae.pendente_por = None
                    tarefaMae.save()
            elif request.POST['processo_relacionado'] == '51' and request.POST['status_processo'] == 'Concluído' and request.POST['stat'] == "Feito":
                tarefa = FormTarefa.save(commit=False)
                tarefa.save()

                # Executores #
                # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                # Valida e salva
                if FormExecutor.is_valid():
                    executores = FormExecutor.save(commit=False)
                    executores.save()
                else:
                    print(FormExecutor.errors)

                try:
                    if request.POST['duplicar'] == '1':

                        # Nova tarefa #
                        try:
                            checado = Pessoa.objects.get(id_pessoa = request.POST['checado'])
                        except:
                            checado = None

                        new_tarefa = Tarefa(
                            id_empresa = usuario.id_empresa,
                            descri = tarefa.descri,
                            id_centro_custo = tarefa.id_centro_custo,
                            prioridade = tarefa.prioridade,
                            stat = "A fazer",
                            id_tamanho = tarefa.id_tamanho,
                            porcentagem = 0,
                            prazo = tarefa.prazo,
                            data_ini = tarefa.data_fim + timedelta(days = int(request.POST['dias'])),
                            data_real = tarefa.data_fim + timedelta(days = int(request.POST['dias'])),
                            # Acrescenta +3 dias a partir da finalização da anterior.
                            data_fim = tarefa.data_fim + timedelta(days = int(request.POST['dias']) + tarefa.prazo),
                            data_finalizacao = tarefa.data_fim + timedelta(days = int(request.POST['dias']) + tarefa.prazo),
                            data_finalizacao_sat = tarefa.data_fim + timedelta(days = int(request.POST['dias']) + tarefa.prazo),
                            status_pendencia = "",
                            historico = "{}\n{}".format(tarefa.status_pendencia, tarefa.historico),
                            id_departamento = tarefa.id_departamento,
                            responsavel = Pessoa.objects.get(id_pessoa = request.POST['responsavel']),
                            autoridade = Pessoa.objects.get(id_pessoa = request.POST['autoridade']),
                            checado = checado,
                            processo_relacionado = tarefa.processo_relacionado,
                            id_pessoa = tarefa.id_pessoa,
                            last_update = datetime.now(),
                            id_update = tarefa.id_update,
                            retrospec = tarefa.retrospec,
                        )
                        new_tarefa.save()

                        # Executores #
                        try:
                            executor1 = Pessoa.objects.get(id_pessoa = request.POST['executor1'])
                        except:
                            executor1 = None
                        try:
                            executor2 = Pessoa.objects.get(id_pessoa = request.POST['executor2'])
                        except:
                            executor2 = None
                        try:
                            executor3 = Pessoa.objects.get(id_pessoa = request.POST['executor3'])
                        except:
                            executor3 = None
                        try:
                            executor4 = Pessoa.objects.get(id_pessoa = request.POST['executor4'])
                        except:
                            executor4 = None
                        try:
                            executor5 = Pessoa.objects.get(id_pessoa = request.POST['executor5'])
                        except:
                            executor5 = None
                        try:
                            executor6 = Pessoa.objects.get(id_pessoa = request.POST['executor6'])
                        except:
                            executor6 = None
                        try:
                            executor7 = Pessoa.objects.get(id_pessoa = request.POST['executor7'])
                        except:
                            executor7 = None
                        try:
                            executor8 = Pessoa.objects.get(id_pessoa = request.POST['executor8'])
                        except:
                            executor8 = None
                        try:
                            executor9 = Pessoa.objects.get(id_pessoa = request.POST['executor9'])
                        except:
                            executor9 = None
                        try:
                            executor10 = Pessoa.objects.get(id_pessoa = request.POST['executor10'])
                        except:
                            executor10 = None

                        new_executores = Executor(
                            executor1 = executor1,
                            porcento1 = executores.porcento1,
                            executor2 = executor2,
                            porcento2 = executores.porcento2,
                            executor3 = executor3,
                            porcento3 = executores.porcento3,
                            executor4 = executor4,
                            porcento4 = executores.porcento4,
                            executor5 = executor5,
                            porcento5 = executores.porcento5,
                            executor6 = executor6,
                            porcento6 = executores.porcento6,
                            executor7 = executor7,
                            porcento7 = executores.porcento7,
                            executor8 = executor8,
                            porcento8 = executores.porcento8,
                            executor9 = executor9,
                            porcento9 = executores.porcento9,
                            executor10 = executor10,
                            porcento10 = executores.porcento10,
                            id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                        )
                        new_executores.save()

                        # Solicitação
                        id_tarefa = Tarefa.objects.get(pk = new_tarefa.id_tarefa)
                        empreendimento = request.POST['empreendimento']
                        bloco = request.POST['bloco']
                        unidade = request.POST['unidade']
                        proprietario_nome = request.POST['proprietario_nome']
                        proprietario_cpf = request.POST['proprietario_cpf']
                        proprietario_rg = request.POST['proprietario_rg']
                        proprietario_email = request.POST['proprietario_email']
                        solicitante_nome = request.POST['solicitante_nome']
                        solicitante_cpf = request.POST['solicitante_cpf']
                        solicitante_rg = request.POST['solicitante_rg']
                        solicitante_email = request.POST['solicitante_email']
                        telefone1 = request.POST['telefone1']
                        telefone2 = request.POST['telefone2']
                        status_processo = 'Agendamento'
                        aux = request.POST['data_finalizacao_sat']
                        data_finalizacao_sat = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                        aux = request.POST['data_entrega']
                        data_entrega = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                        tipo_solicitacao = request.POST['tipo_solicitacao']
                        tempo_total = request.POST['tempo_total']
                        satisfacao_avaliacao = request.POST['satisfacao_avaliacao']

                        solicitacao = Solicitacao(id_tarefa=id_tarefa, empreendimento=empreendimento, bloco=bloco, unidade=unidade, proprietario_nome=proprietario_nome, proprietario_cpf=proprietario_cpf, proprietario_rg=proprietario_rg, proprietario_email=proprietario_email, 
                        solicitante_nome=solicitante_nome, solicitante_cpf=solicitante_cpf, solicitante_rg=solicitante_rg, solicitante_email=solicitante_email, telefone1=telefone1, telefone2=telefone2, status_processo=status_processo, data_finalizacao_sat=data_finalizacao_sat, 
                        data_entrega=data_entrega, tipo_solicitacao=tipo_solicitacao, tempo_total=tempo_total, satisfacao_avaliacao=satisfacao_avaliacao
                        )
                        solicitacao.save()

                        # Problemas
                        try:
                            print("ambiente1: {}".format(request.POST['ambiente1']))
                            if request.POST['ambiente1'] != "":
                                for j in range(int(request.POST['qtdProblemas'])):
                                    ambiente = request.POST['ambiente'+ str(j + 1)]
                                    descricao_sat = request.POST['descricao_sat'+ str(j + 1)]
                                    tipo_reparo = request.POST['tipo_reparo'+ str(j + 1)]
                                    historico_sat = request.POST['historico_sat'+ str(j + 1)]
                                    procedencia = request.POST['procedencia'+ str(j + 1)]
                                    estimativa_custo = request.POST['estimativa_custo'+ str(j + 1)]
                                    material = request.POST['material'+ str(j + 1)]
                                    duracao = request.POST['duracao'+ str(j + 1)]
                                    finalizado = 0

                                    problema = Problema(id_solicitacao=solicitacao, ambiente=ambiente, descricao_sat=descricao_sat, tipo_reparo=tipo_reparo, historico_sat=historico_sat, procedencia=procedencia, 
                                    estimativa_custo=estimativa_custo, material=material, duracao=duracao, finalizado=finalizado)
                                    problema.save()
                            else:
                                problema = Problema(id_solicitacao=solicitacao)
                                problema.save()
                        except:
                            problema = Problema(id_solicitacao=solicitacao)
                            problema.save()
                except:
                    print('Não selecionado')
            elif request.POST['processo_relacionado'] == '29':
                if id_stats == 1:
                    tarefa.id_status = 1
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)
                elif tarefa.id_status == 2 and tarefa.stat == "Feito" and statusLocacao != "Feito":
                    id_juridico = tarefa.id_juridico
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)
                    
                    # Nova tarefa #
                    tarefa_mae = get_object_or_404(Tarefa, pk=id_juridico)

                    new_tarefa = Tarefa(
                        id_empresa = usuario.id_empresa,
                        descri = 'Defesa: ' + str(id_juridico) + " - " + tarefa_mae.descri,
                        id_centro_custo = tarefa.id_centro_custo,
                        prioridade = tarefa.prioridade,
                        stat = "A fazer",
                        id_tamanho = tarefa.id_tamanho,
                        porcentagem = 0,
                        prazo = tarefa.prazo,
                        data_ini = tarefa.data_fim,
                        data_real = tarefa.data_fim,
                        # Acrescenta +3 dias a partir da finalização da anterior.
                        data_fim = tarefa.data_fim,
                        data_finalizacao = tarefa.data_finalizacao,
                        data_finalizacao_sat = tarefa.data_finalizacao_sat,
                        status_pendencia = "",
                        historico = "",
                        id_departamento = tarefa.id_departamento,
                        responsavel = tarefa.responsavel,
                        autoridade = tarefa.autoridade,
                        processo_relacionado = tarefa.processo_relacionado,
                        id_pessoa = tarefa.id_pessoa,
                        last_update = datetime.now(),
                        id_update = tarefa.id_update,
                        etapa = tarefa.etapa,
                        subetapa = tarefa.subetapa,
                        retrospec = tarefa.retrospec,
                        id_juridico = id_juridico,
                        id_status = 3,
                    )
                    new_tarefa.save()

                    # Executores #
                    new_executores = Executor(
                        executor1 = executores.executor1,
                        porcento1 = executores.porcento1,
                        executor2 = executores.executor2,
                        porcento2 = executores.porcento2,
                        executor3 = executores.executor3,
                        porcento3 = executores.porcento3,
                        executor4 = executores.executor4,
                        porcento4 = executores.porcento4,
                        executor5 = executores.executor5,
                        porcento5 = executores.porcento5,
                        executor6 = executores.executor6,
                        porcento6 = executores.porcento6,
                        executor7 = executores.executor7,
                        porcento7 = executores.porcento7,
                        executor8 = executores.executor8,
                        porcento8 = executores.porcento8,
                        executor9 = executores.executor9,
                        porcento9 = executores.porcento9,
                        executor10 = executores.executor10,
                        porcento10 = executores.porcento10,
                        id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                    )
                    new_executores.save()
                elif tarefa.id_status == 3 and tarefa.stat == "Feito" and statusLocacao != "Feito":
                    id_juridico = tarefa.id_juridico
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)
                    
                    # Nova tarefa #
                    tarefa_mae = get_object_or_404(Tarefa, pk=id_juridico)

                    new_tarefa = Tarefa(
                        id_empresa = usuario.id_empresa,
                        descri = 'Réplica: ' + str(id_juridico) + " - " + tarefa_mae.descri,
                        id_centro_custo = tarefa.id_centro_custo,
                        prioridade = tarefa.prioridade,
                        stat = "A fazer",
                        id_tamanho = tarefa.id_tamanho,
                        porcentagem = 0,
                        prazo = tarefa.prazo,
                        data_ini = tarefa.data_fim,
                        data_real = tarefa.data_fim,
                        # Acrescenta +3 dias a partir da finalização da anterior.
                        data_fim = tarefa.data_fim,
                        data_finalizacao = tarefa.data_finalizacao,
                        data_finalizacao_sat = tarefa.data_finalizacao_sat,
                        status_pendencia = "",
                        historico = "",
                        id_departamento = tarefa.id_departamento,
                        responsavel = tarefa.responsavel,
                        autoridade = tarefa.autoridade,
                        processo_relacionado = tarefa.processo_relacionado,
                        id_pessoa = tarefa.id_pessoa,
                        last_update = datetime.now(),
                        id_update = tarefa.id_update,
                        etapa = tarefa.etapa,
                        subetapa = tarefa.subetapa,
                        retrospec = tarefa.retrospec,
                        id_juridico = id_juridico,
                        id_status = 4,
                    )
                    new_tarefa.save()

                    # Executores #
                    new_executores = Executor(
                        executor1 = executores.executor1,
                        porcento1 = executores.porcento1,
                        executor2 = executores.executor2,
                        porcento2 = executores.porcento2,
                        executor3 = executores.executor3,
                        porcento3 = executores.porcento3,
                        executor4 = executores.executor4,
                        porcento4 = executores.porcento4,
                        executor5 = executores.executor5,
                        porcento5 = executores.porcento5,
                        executor6 = executores.executor6,
                        porcento6 = executores.porcento6,
                        executor7 = executores.executor7,
                        porcento7 = executores.porcento7,
                        executor8 = executores.executor8,
                        porcento8 = executores.porcento8,
                        executor9 = executores.executor9,
                        porcento9 = executores.porcento9,
                        executor10 = executores.executor10,
                        porcento10 = executores.porcento10,
                        id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                    )
                    new_executores.save()
                elif tarefa.id_status == 4 and tarefa.stat == "Feito" and statusLocacao != "Feito":
                    id_juridico = tarefa.id_juridico
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)
                    
                    # Nova tarefa #
                    tarefa_mae = get_object_or_404(Tarefa, pk=id_juridico)

                    new_tarefa = Tarefa(
                        id_empresa = usuario.id_empresa,
                        descri = 'Audiência: ' + str(id_juridico) + " - " + tarefa_mae.descri,
                        id_centro_custo = tarefa.id_centro_custo,
                        prioridade = tarefa.prioridade,
                        stat = "A fazer",
                        id_tamanho = tarefa.id_tamanho,
                        porcentagem = 0,
                        prazo = tarefa.prazo,
                        data_ini = tarefa.data_fim,
                        data_real = tarefa.data_fim,
                        # Acrescenta +3 dias a partir da finalização da anterior.
                        data_fim = tarefa.data_fim,
                        data_finalizacao = tarefa.data_finalizacao,
                        data_finalizacao_sat = tarefa.data_finalizacao_sat,
                        status_pendencia = "",
                        historico = "",
                        id_departamento = tarefa.id_departamento,
                        responsavel = tarefa.responsavel,
                        autoridade = tarefa.autoridade,
                        processo_relacionado = tarefa.processo_relacionado,
                        id_pessoa = tarefa.id_pessoa,
                        last_update = datetime.now(),
                        id_update = tarefa.id_update,
                        etapa = tarefa.etapa,
                        subetapa = tarefa.subetapa,
                        retrospec = tarefa.retrospec,
                        id_juridico = id_juridico,
                        id_status = 5,
                    )
                    new_tarefa.save()

                    # Executores #
                    new_executores = Executor(
                        executor1 = executores.executor1,
                        porcento1 = executores.porcento1,
                        executor2 = executores.executor2,
                        porcento2 = executores.porcento2,
                        executor3 = executores.executor3,
                        porcento3 = executores.porcento3,
                        executor4 = executores.executor4,
                        porcento4 = executores.porcento4,
                        executor5 = executores.executor5,
                        porcento5 = executores.porcento5,
                        executor6 = executores.executor6,
                        porcento6 = executores.porcento6,
                        executor7 = executores.executor7,
                        porcento7 = executores.porcento7,
                        executor8 = executores.executor8,
                        porcento8 = executores.porcento8,
                        executor9 = executores.executor9,
                        porcento9 = executores.porcento9,
                        executor10 = executores.executor10,
                        porcento10 = executores.porcento10,
                        id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                    )
                    new_executores.save()
                elif tarefa.id_status == 5 and tarefa.stat == "Feito" and statusLocacao != "Feito":
                    id_juridico = tarefa.id_juridico
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)
                    
                    # Nova tarefa #
                    tarefa_mae = get_object_or_404(Tarefa, pk=id_juridico)

                    new_tarefa = Tarefa(
                        id_empresa = usuario.id_empresa,
                        descri = 'Alegações Finais: ' + str(id_juridico) + " - " + tarefa_mae.descri,
                        id_centro_custo = tarefa.id_centro_custo,
                        prioridade = tarefa.prioridade,
                        stat = "A fazer",
                        id_tamanho = tarefa.id_tamanho,
                        porcentagem = 0,
                        prazo = tarefa.prazo,
                        data_ini = tarefa.data_fim,
                        data_real = tarefa.data_fim,
                        # Acrescenta +3 dias a partir da finalização da anterior.
                        data_fim = tarefa.data_fim,
                        data_finalizacao = tarefa.data_finalizacao,
                        data_finalizacao_sat = tarefa.data_finalizacao_sat,
                        status_pendencia = "",
                        historico = "",
                        id_departamento = tarefa.id_departamento,
                        responsavel = tarefa.responsavel,
                        autoridade = tarefa.autoridade,
                        processo_relacionado = tarefa.processo_relacionado,
                        id_pessoa = tarefa.id_pessoa,
                        last_update = datetime.now(),
                        id_update = tarefa.id_update,
                        etapa = tarefa.etapa,
                        subetapa = tarefa.subetapa,
                        retrospec = tarefa.retrospec,
                        id_juridico = id_juridico,
                        id_status = 6,
                    )
                    new_tarefa.save()

                    # Executores #
                    new_executores = Executor(
                        executor1 = executores.executor1,
                        porcento1 = executores.porcento1,
                        executor2 = executores.executor2,
                        porcento2 = executores.porcento2,
                        executor3 = executores.executor3,
                        porcento3 = executores.porcento3,
                        executor4 = executores.executor4,
                        porcento4 = executores.porcento4,
                        executor5 = executores.executor5,
                        porcento5 = executores.porcento5,
                        executor6 = executores.executor6,
                        porcento6 = executores.porcento6,
                        executor7 = executores.executor7,
                        porcento7 = executores.porcento7,
                        executor8 = executores.executor8,
                        porcento8 = executores.porcento8,
                        executor9 = executores.executor9,
                        porcento9 = executores.porcento9,
                        executor10 = executores.executor10,
                        porcento10 = executores.porcento10,
                        id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                    )
                    new_executores.save()
                elif tarefa.id_status == 6 and tarefa.stat == "Feito" and statusLocacao != "Feito":
                    id_juridico = tarefa.id_juridico
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)
                    
                    # Nova tarefa #
                    tarefa_mae = get_object_or_404(Tarefa, pk=id_juridico)

                    new_tarefa = Tarefa(
                        id_empresa = usuario.id_empresa,
                        descri = 'Sentença: ' + str(id_juridico) + " - " + tarefa_mae.descri,
                        id_centro_custo = tarefa.id_centro_custo,
                        prioridade = tarefa.prioridade,
                        stat = "A fazer",
                        id_tamanho = tarefa.id_tamanho,
                        porcentagem = 0,
                        prazo = tarefa.prazo,
                        data_ini = tarefa.data_fim,
                        data_real = tarefa.data_fim,
                        # Acrescenta +3 dias a partir da finalização da anterior.
                        data_fim = tarefa.data_fim,
                        data_finalizacao = tarefa.data_finalizacao,
                        data_finalizacao_sat = tarefa.data_finalizacao_sat,
                        status_pendencia = "",
                        historico = "",
                        id_departamento = tarefa.id_departamento,
                        responsavel = tarefa.responsavel,
                        autoridade = tarefa.autoridade,
                        processo_relacionado = tarefa.processo_relacionado,
                        id_pessoa = tarefa.id_pessoa,
                        last_update = datetime.now(),
                        id_update = tarefa.id_update,
                        etapa = tarefa.etapa,
                        subetapa = tarefa.subetapa,
                        retrospec = tarefa.retrospec,
                        id_juridico = id_juridico,
                        id_status = 7,
                    )
                    new_tarefa.save()

                    # Executores #
                    new_executores = Executor(
                        executor1 = executores.executor1,
                        porcento1 = executores.porcento1,
                        executor2 = executores.executor2,
                        porcento2 = executores.porcento2,
                        executor3 = executores.executor3,
                        porcento3 = executores.porcento3,
                        executor4 = executores.executor4,
                        porcento4 = executores.porcento4,
                        executor5 = executores.executor5,
                        porcento5 = executores.porcento5,
                        executor6 = executores.executor6,
                        porcento6 = executores.porcento6,
                        executor7 = executores.executor7,
                        porcento7 = executores.porcento7,
                        executor8 = executores.executor8,
                        porcento8 = executores.porcento8,
                        executor9 = executores.executor9,
                        porcento9 = executores.porcento9,
                        executor10 = executores.executor10,
                        porcento10 = executores.porcento10,
                        id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                    )
                    new_executores.save()
                elif tarefa.id_status == 7 and tarefa.stat == "Feito" and statusLocacao != "Feito":
                    id_juridico = tarefa.id_juridico
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)
                    
                    # Nova tarefa #
                    tarefa_mae = get_object_or_404(Tarefa, pk=id_juridico)

                    new_tarefa = Tarefa(
                        id_empresa = usuario.id_empresa,
                        descri = 'Recurso - 2ª Instância: ' + str(id_juridico) + " - " + tarefa_mae.descri,
                        id_centro_custo = tarefa.id_centro_custo,
                        prioridade = tarefa.prioridade,
                        stat = "A fazer",
                        id_tamanho = tarefa.id_tamanho,
                        porcentagem = 0,
                        prazo = tarefa.prazo,
                        data_ini = tarefa.data_fim,
                        data_real = tarefa.data_fim,
                        # Acrescenta +3 dias a partir da finalização da anterior.
                        data_fim = tarefa.data_fim,
                        data_finalizacao = tarefa.data_finalizacao,
                        data_finalizacao_sat = tarefa.data_finalizacao_sat,
                        status_pendencia = "",
                        historico = "",
                        id_departamento = tarefa.id_departamento,
                        responsavel = tarefa.responsavel,
                        autoridade = tarefa.autoridade,
                        processo_relacionado = tarefa.processo_relacionado,
                        id_pessoa = tarefa.id_pessoa,
                        last_update = datetime.now(),
                        id_update = tarefa.id_update,
                        etapa = tarefa.etapa,
                        subetapa = tarefa.subetapa,
                        retrospec = tarefa.retrospec,
                        id_juridico = id_juridico,
                        id_status = 8,
                    )
                    new_tarefa.save()

                    # Executores #
                    new_executores = Executor(
                        executor1 = executores.executor1,
                        porcento1 = executores.porcento1,
                        executor2 = executores.executor2,
                        porcento2 = executores.porcento2,
                        executor3 = executores.executor3,
                        porcento3 = executores.porcento3,
                        executor4 = executores.executor4,
                        porcento4 = executores.porcento4,
                        executor5 = executores.executor5,
                        porcento5 = executores.porcento5,
                        executor6 = executores.executor6,
                        porcento6 = executores.porcento6,
                        executor7 = executores.executor7,
                        porcento7 = executores.porcento7,
                        executor8 = executores.executor8,
                        porcento8 = executores.porcento8,
                        executor9 = executores.executor9,
                        porcento9 = executores.porcento9,
                        executor10 = executores.executor10,
                        porcento10 = executores.porcento10,
                        id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                    )
                    new_executores.save()
                elif tarefa.id_status == 8 and tarefa.stat == "Feito" and statusLocacao != "Feito":
                    id_juridico = tarefa.id_juridico
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)
                    
                    # Nova tarefa #
                    tarefa_mae = get_object_or_404(Tarefa, pk=id_juridico)

                    new_tarefa = Tarefa(
                        id_empresa = usuario.id_empresa,
                        descri = 'Recurso - 3ª Instância: ' + str(id_juridico) + " - " + tarefa_mae.descri,
                        id_centro_custo = tarefa.id_centro_custo,
                        prioridade = tarefa.prioridade,
                        stat = "A fazer",
                        id_tamanho = tarefa.id_tamanho,
                        porcentagem = 0,
                        prazo = tarefa.prazo,
                        data_ini = tarefa.data_fim,
                        data_real = tarefa.data_fim,
                        # Acrescenta +3 dias a partir da finalização da anterior.
                        data_fim = tarefa.data_fim,
                        data_finalizacao = tarefa.data_finalizacao,
                        data_finalizacao_sat = tarefa.data_finalizacao_sat,
                        status_pendencia = "",
                        historico = "",
                        id_departamento = tarefa.id_departamento,
                        responsavel = tarefa.responsavel,
                        autoridade = tarefa.autoridade,
                        processo_relacionado = tarefa.processo_relacionado,
                        id_pessoa = tarefa.id_pessoa,
                        last_update = datetime.now(),
                        id_update = tarefa.id_update,
                        etapa = tarefa.etapa,
                        subetapa = tarefa.subetapa,
                        retrospec = tarefa.retrospec,
                        id_juridico = id_juridico,
                        id_status = 9,
                    )
                    new_tarefa.save()

                    # Executores #
                    new_executores = Executor(
                        executor1 = executores.executor1,
                        porcento1 = executores.porcento1,
                        executor2 = executores.executor2,
                        porcento2 = executores.porcento2,
                        executor3 = executores.executor3,
                        porcento3 = executores.porcento3,
                        executor4 = executores.executor4,
                        porcento4 = executores.porcento4,
                        executor5 = executores.executor5,
                        porcento5 = executores.porcento5,
                        executor6 = executores.executor6,
                        porcento6 = executores.porcento6,
                        executor7 = executores.executor7,
                        porcento7 = executores.porcento7,
                        executor8 = executores.executor8,
                        porcento8 = executores.porcento8,
                        executor9 = executores.executor9,
                        porcento9 = executores.porcento9,
                        executor10 = executores.executor10,
                        porcento10 = executores.porcento10,
                        id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                    )
                    new_executores.save()
                elif tarefa.id_status == 9 and tarefa.stat == "Feito" and statusLocacao != "Feito":
                    id_juridico = tarefa.id_juridico
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)
                else:
                    tarefa.save()

                    # Executores #
                    # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                    executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                    FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                    # Valida e salva
                    if FormExecutor.is_valid():
                        executores = FormExecutor.save(commit=False)
                        executores.save()
                    else:
                        print(FormExecutor.errors)

                tarefasFilhas = Tarefa.objects.filter(id_juridico=tarefa.id_juridico)
                qtdFeito = 0

                for filha in tarefasFilhas:
                    if(filha.stat == "Feito"):
                        qtdFeito += 1
                qtdFeito = len(tarefasFilhas) - qtdFeito
                if(qtdFeito == 1):
                    tarefa_mae = get_object_or_404(Tarefa, pk=tarefa.id_juridico)
                    tarefa_mae.stat = "Feito"
                    tarefa_mae.porcentagem = 100
                    tarefa_mae.data_fim = date.today()
                    tarefa_mae.historico = tarefa_mae.status_pendencia + "\n" + tarefa_mae.historico
                    tarefa_mae.status_pendencia = ""
                    tarefa_mae.pendente_por = None
                    tarefa_mae.save()
            elif request.POST['processo_relacionado'] == '146':
                tarefa.id_status = 11
                tarefa.id_locacao = tarefa.id_tarefa
                tarefa = FormTarefa.save(commit=False)
                tarefa.save()

                # Executores #
                # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                # Valida e salva
                if FormExecutor.is_valid():
                    executores = FormExecutor.save(commit=False)
                    executores.save()
                else:
                    print(FormExecutor.errors)
                
                if (locacao == ""):
                    if (request.POST['lBloco'] != "---"):
                        id_tarefa = tarefa.id_locacao
                        bloco = request.POST['lBloco']
                        unidade = request.POST['lUnidade']

                        locacao = Locacao(id_tarefa=id_tarefa, lBloco=bloco, lUnidade=unidade)
                        locacao.save()
                    else:
                        print("Não há locacao")
                else:
                    if (tarefa.id_locacao != None):
                        locacao = get_object_or_404(Locacao, id_tarefa=request.POST['id_locacao'])
                        locacao.id_tarefa = tarefa.id_locacao
                        locacao.lBloco = request.POST['lBloco']
                        locacao.lUnidade = request.POST['lUnidade']

                        tarefa.id_locacao = tarefa.id_locacao
                        tarefa.save()

                        locacao.save()
            elif request.POST['id_filho'] != '':
                tarefa.save()
                print('teste filho')
                # Executores #
                # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                # Valida e salva
                if FormExecutor.is_valid():
                    executores = FormExecutor.save(commit=False)
                    executores.save()
                else:
                    print(FormExecutor.errors)
                
                tarefasFilhas = Tarefa.objects.filter(id_filho=tarefa.id_filho).order_by('id_tarefa')

                for filha in tarefasFilhas:
                    if filhosTarefa != "" and len(filhosTarefa) != 0 and (filha.stat != 'Feito' and filha.stat != 'Cancelado') and tarefa.id_status == 0:
                        if filha.id_tarefa != tarefa.id_tarefa and filha.id_tarefa != tarefa.id_filho :
                            filha.stat = request.POST['stat{}'.format(filha.id_tarefa)]
                            filha.porcentagem = request.POST['porcentagem{}'.format(filha.id_tarefa)]
                            data_ini = request.POST['data_ini{}'.format(filha.id_tarefa)].split('/')
                            filha.data_ini = "{}-{}-{}".format(data_ini[2], data_ini[1], data_ini[0])
                            data_fim = request.POST['data_fim{}'.format(filha.id_tarefa)].split('/')
                            filha.data_fim = "{}-{}-{}".format(data_fim[2], data_fim[1], data_fim[0])
                            filha.id_tamanho = Tamanho.objects.get(id_tamanho = request.POST['tamanho{}'.format(filha.id_tarefa)])
                            filha.status_pendencia = request.POST['status_pendencia{}'.format(filha.id_tarefa)]
                            filha.historico = request.POST['historico{}'.format(filha.id_tarefa)]

                            if filha.stat == "A fazer":
                                filha.porcentagem = 0
                            if filha.stat == "Fazendo" and request.POST['porcentagem{}'.format(filha.id_tarefa)] == '0':
                                filha.porcentagem = 1
                            if filha.stat == "Feito":
                                filha.porcentagem = 100

                            filha.save()
            else:
                tarefa.id_status = None
                tarefa.save()

                # Executores #
                # Buscando a instancia da tarefa e criando o form carregando os dados do POST
                executores = get_object_or_404(Executor, id_tarefa=request.POST['id_tarefa'])
                FormExecutor = ExecutorFormsEditar(request, request.POST, instance=executores)

                # Valida e salva
                if FormExecutor.is_valid():
                    executores = FormExecutor.save(commit=False)
                    executores.save()
                else:
                    print(FormExecutor.errors)

            if (retrospectiva == ""):
                if (request.POST['classificacao'] != ""):
                    id_tarefa = Tarefa.objects.get(pk = request.POST['idTarefa'])
                    descricao = request.POST['classificacao']
                    stats = request.POST['rStat']
                    rResponsavel = request.POST['id_responsavel']

                    id_pessoa_objects = Pessoa.objects.all().filter(id_user=request.user.id)
                    id_update = id_pessoa_objects[0]
                    id_pessoa_objects = Pessoa.objects.all().filter(id_pessoa=rResponsavel)
                    rResponsavel = id_pessoa_objects[0]
                    nome_responsavel = id_pessoa_objects[0].nome
                    last_update = datetime.now()

                    retrospectiva = Retrospectiva(id_tarefa=id_tarefa, descricao=descricao, stats=stats, finalizado=0, id_update=id_update, last_update=last_update, id_responsavel=rResponsavel, nome_responsavel=nome_responsavel)
                    retrospectiva.save()
                    # print("Retrospectiva cadastrada!")
                else:
                    print("Não há retrospectiva!")
            else:
                retrospectiva = get_object_or_404(Retrospectiva, id_tarefa=id)
                retrospectiva.id_tarefa = Tarefa.objects.get(pk = request.POST['idTarefa'])
                retrospectiva.descricao = request.POST['classificacao']
                retrospectiva.stats = request.POST['rStat']
                retrospectiva.finalizado = request.POST['finalizado']
                rResponsavel = request.POST['id_responsavel']

                id_pessoa_objects = Pessoa.objects.all().filter(id_pessoa=rResponsavel)
                rResponsavel = id_pessoa_objects[0]
                retrospectiva.id_responsavel = rResponsavel
                retrospectiva.nome_responsavel = id_pessoa_objects[0].nome

                retrospectiva.save()

            if (r5w2h == ""):
                if (request.POST['rWhat'] != ""):
                    id_tarefa = Tarefa.objects.get(pk = request.POST['idTarefa'])
                    rWhat = request.POST['rWhat']
                    rWhy = request.POST['rWhy']
                    rWhere = request.POST['rWhere']
                    rWhen = request.POST['rWhen']
                    rWho = request.POST['rWho']
                    rHow = request.POST['rHow']
                    rHowMuch = request.POST['rHowMuch']

                    id_pessoa_objects = Pessoa.objects.all().filter(id_user=request.user.id)
                    id_update = id_pessoa_objects[0]
                    last_update = datetime.now()

                    r5w2h = R5w2h(id_tarefa=id_tarefa, rWhat=rWhat, rWhy=rWhy, rWhere=rWhere, rWhen=rWhen, rWho=rWho, rHow=rHow, rHowMuch=rHowMuch, id_update=id_update, last_update=last_update)
                    r5w2h.save()
                    # print("5w2h cadastrado!")
                else:
                    print("Não há 5w2h!")
            else:
                r5w2h = get_object_or_404(R5w2h, id_tarefa=id)
                r5w2h.id_tarefa = Tarefa.objects.get(pk = request.POST['idTarefa'])
                r5w2h.rWhat = request.POST['rWhat']
                r5w2h.rWhy = request.POST['rWhy']
                r5w2h.rWhere = request.POST['rWhere']
                r5w2h.rWhen = request.POST['rWhen']
                r5w2h.rWho = request.POST['rWho']
                r5w2h.rHow = request.POST['rHow']
                r5w2h.rHowMuch = request.POST['rHowMuch']
                
                r5w2h.save()
                # print("r5w2h atualizado!")

            if (solicitacao == ""):
                if (request.POST['proprietario_nome'] != ""):
                    id_tarefa = Tarefa.objects.get(pk = request.POST['idTarefa'])
                    empreendimento = request.POST['empreendimento']
                    bloco = request.POST['bloco']
                    unidade = request.POST['unidade']
                    proprietario_nome = request.POST['proprietario_nome']
                    proprietario_cpf = request.POST['proprietario_cpf']
                    proprietario_rg = request.POST['proprietario_rg']
                    proprietario_email = request.POST['proprietario_email']
                    solicitante_nome = request.POST['solicitante_nome']
                    solicitante_cpf = request.POST['solicitante_cpf']
                    solicitante_rg = request.POST['solicitante_rg']
                    solicitante_email = request.POST['solicitante_email']
                    telefone1 = request.POST['telefone1']
                    telefone2 = request.POST['telefone2']
                    status_processo = request.POST['status_processo']
                    aux = request.POST['data_finalizacao_sat']
                    data_finalizacao_sat = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                    aux = request.POST['data_entrega']
                    data_entrega = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                    tipo_solicitacao = request.POST['tipo_solicitacao']
                    tempo_total = request.POST['tempo_total']
                    satisfacao_avaliacao = request.POST['satisfacao_avaliacao']

                    solicitacao = Solicitacao(id_tarefa=id_tarefa, empreendimento=empreendimento, bloco=bloco, unidade=unidade, proprietario_nome=proprietario_nome, proprietario_cpf=proprietario_cpf, proprietario_rg=proprietario_rg, proprietario_email=proprietario_email, 
                    solicitante_nome=solicitante_nome, solicitante_cpf=solicitante_cpf, solicitante_rg=solicitante_rg, solicitante_email=solicitante_email, telefone1=telefone1, telefone2=telefone2, status_processo=status_processo, data_finalizacao_sat=data_finalizacao_sat, 
                    data_entrega=data_entrega, tipo_solicitacao=tipo_solicitacao, tempo_total=tempo_total, satisfacao_avaliacao=satisfacao_avaliacao
                    )
                    solicitacao.save()
                else:
                    print("Não há solicitação")
            else:
                solicitacao = get_object_or_404(Solicitacao, id_tarefa=id)
                solicitacao.id_tarefa = Tarefa.objects.get(pk = request.POST['idTarefa'])
                solicitacao.empreendimento = request.POST['empreendimento']
                solicitacao.bloco = request.POST['bloco']
                solicitacao.unidade = request.POST['unidade']
                solicitacao.proprietario_nome = request.POST['proprietario_nome']
                solicitacao.proprietario_cpf = request.POST['proprietario_cpf']
                solicitacao.proprietario_rg = request.POST['proprietario_rg']
                solicitacao.proprietario_email = request.POST['proprietario_email']
                solicitacao.solicitante_nome = request.POST['solicitante_nome']
                solicitacao.solicitante_cpf = request.POST['solicitante_cpf']
                solicitacao.solicitante_rg = request.POST['solicitante_rg']
                solicitacao.solicitante_email = request.POST['solicitante_email']
                solicitacao.telefone1 = request.POST['telefone1']
                solicitacao.telefone2 = request.POST['telefone2']
                solicitacao.status_processo = request.POST['status_processo']
                aux = request.POST['data_finalizacao_sat']
                solicitacao.data_finalizacao_sat = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                aux = request.POST['data_entrega']
                solicitacao.data_entrega = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                solicitacao.tipo_solicitacao = request.POST['tipo_solicitacao']
                solicitacao.tempo_total = request.POST['tempo_total']
                solicitacao.satisfacao_avaliacao = request.POST['satisfacao_avaliacao']

                solicitacao.save()

            if (problema == ""):
                try:
                    for j in range(int(request.POST['qtdProblemas'])):
                        id_solicitacao = solicitacao

                        ambiente = request.POST['ambiente'+ str(j + 1)]
                        descricao_sat = request.POST['descricao_sat'+ str(j + 1)]
                        tipo_reparo = request.POST['tipo_reparo'+ str(j + 1)]
                        historico_sat = request.POST['historico_sat'+ str(j + 1)]
                        procedencia = request.POST['procedencia'+ str(j + 1)]
                        estimativa_custo = request.POST['estimativa_custo'+ str(j + 1)]
                        material = request.POST['material'+ str(j + 1)]
                        duracao = request.POST['duracao'+ str(j + 1)]
                        try:
                            finalizado = request.POST['finalizado'+ str(j + 1)]
                            finalizado = 1
                        except:
                            finalizado = 0

                        problema = Problema(id_solicitacao=id_solicitacao, ambiente=ambiente, descricao_sat=descricao_sat, tipo_reparo=tipo_reparo, historico_sat=historico_sat, procedencia=procedencia, 
                        estimativa_custo=estimativa_custo, material=material, duracao=duracao, finalizado=finalizado)
                        problema.save()
                except:
                    print("Não há problema")
            else:
                problemas = Problema.objects.filter(id_solicitacao=solicitacao.id_solicitacao)
                i = 0
                try:
                    for problema in problemas:
                        i += 1
                        problema.ambiente = request.POST['ambiente'+ str(i)]
                        problema.descricao_sat = request.POST['descricao_sat'+ str(i)]
                        problema.tipo_reparo = request.POST['tipo_reparo'+ str(i)]
                        problema.historico_sat = request.POST['historico_sat'+ str(i)]
                        problema.procedencia = request.POST['procedencia'+ str(i)]
                        problema.estimativa_custo = request.POST['estimativa_custo'+ str(i)]
                        problema.material = request.POST['material'+ str(i)]
                        problema.duracao = request.POST['duracao'+ str(i)]
                        try:
                            problema.finalizado = request.POST['finalizado'+ str(i)]
                            problema.finalizado = 1
                        except:
                            problema.finalizado = 0

                        problema.save()
                    
                    for j in range(int(request.POST['qtdProblemas']) - i):
                        try:
                            solicitacao_objects = Solicitacao.objects.filter(id_solicitacao=solicitacao.id_solicitacao)
                            id_solicitacao = solicitacao_objects[0]

                            ambiente = request.POST['ambiente'+ str(j + i + 1)]
                            descricao_sat = request.POST['descricao_sat'+ str(j + i + 1)]
                            tipo_reparo = request.POST['tipo_reparo'+ str(j + i + 1)]
                            historico_sat = request.POST['historico_sat'+ str(j + i + 1)]
                            procedencia = request.POST['procedencia'+ str(j + i + 1)]
                            estimativa_custo = request.POST['estimativa_custo'+ str(j + i + 1)]
                            material = request.POST['material'+ str(j + i + 1)]
                            duracao = request.POST['duracao'+ str(j + i + 1)]
                            try:
                                finalizado = request.POST['finalizado'+ str(j + 1)]
                                finalizado = 1
                            except:
                                finalizado = 0

                            problema = Problema(id_solicitacao=id_solicitacao, ambiente=ambiente, descricao_sat=descricao_sat, tipo_reparo=tipo_reparo, historico_sat=historico_sat, procedencia=procedencia, 
                            estimativa_custo=estimativa_custo, material=material, duracao=duracao, finalizado=finalizado)
                            problema.save()
                            print("Problema: " + str(j + i + 1) + " cadastrado!")
                        except:
                            print("Erro ao cadastrar problema")
                except:
                    None

            if (medicao_terceiros == ""):
                if (request.POST['mes'] != '0'):
                    id_tarefa = request.POST['id_tarefa']
                    mes = request.POST['mes']
                    valor_bruto = request.POST['valor_bruto']
                    valor_liquido = request.POST['valor_liquido']
                    permuta = request.POST['permuta']

                    medicao_terceiros = MedicaoTerceiros(id_tarefa=id_tarefa, mes=mes, valor_bruto=valor_bruto, valor_liquido=valor_liquido, permuta=permuta)
                    medicao_terceiros.save()
                else:
                    print("Não há medição de terceiros")
            else:
                medicao_terceiros = get_object_or_404(MedicaoTerceiros, id_tarefa=request.POST['id_tarefa'])
                medicao_terceiros.id_tarefa = request.POST['id_tarefa']
                medicao_terceiros.mes = request.POST['mes']
                medicao_terceiros.valor_bruto = request.POST['valor_bruto']
                medicao_terceiros.valor_liquido = request.POST['valor_liquido']
                medicao_terceiros.permuta = request.POST['permuta']

                medicao_terceiros.save()

            if (juridico == ""):
                if (request.POST['id_resumo_processo'] != ""):
                    id_tarefa = request.POST['id_juridico']
                    escritorio = request.POST['escritorio']
                    escritorio_advogado = request.POST['escritorio_advogado']
                    resumo_processo = request.POST['id_resumo_processo']
                    numero_processo = request.POST['numero_processo']
                    aux = request.POST['prazo_interno']
                    prazo_interno = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                    observacoes = request.POST['id_observacoes']
                    valor_estimado = request.POST['valor_estimado']
                    valor_causa = request.POST['valor_causa']
                    valor_acordo = request.POST['valor_acordo']
                    autor_assistente = request.POST['autor_assistente']
                    autor_advogado = request.POST['autor_advogado']
                    reu_assistente = request.POST['reu_assistente']
                    reu_advogado = request.POST['reu_advogado']
                    perito = request.POST['perito']
                    preposto = request.POST['preposto']
                    jUnidade = request.POST['jUnidade']
                    jBloco = request.POST['jBloco']

                    juridico = Juridico(
                        id_tarefa=id_tarefa,
                        autor_assistente=autor_assistente,
                        autor_advogado=autor_advogado,
                        reu_assistente=reu_assistente,
                        reu_advogado=reu_advogado,
                        escritorio=escritorio,
                        escritorio_advogado=escritorio_advogado,
                        resumo_processo=resumo_processo,
                        numero_processo=numero_processo,
                        prazo_interno=prazo_interno,
                        observacoes=observacoes,
                        valor_estimado=valor_estimado,
                        valor_causa=valor_causa,
                        valor_acordo=valor_acordo,
                        perito=perito,
                        jUnidade=jUnidade,
                        jBloco=jBloco
                    )
                    juridico.save()

                    testemunha1 = request.POST['testemunha1']
                    if request.POST['testemunha2']:
                        testemunha2 = request.POST['testemunha2']
                    else:
                        testemunha2 = None
                    if request.POST['testemunha3']:
                        testemunha3 = request.POST['testemunha3']
                    else:
                        testemunha3 = None
                    if request.POST['testemunha4']:
                        testemunha4 = request.POST['testemunha4']
                    else:
                        testemunha4 = None
                    if request.POST['testemunha5']:
                        testemunha5 = request.POST['testemunha5']
                    else:
                        testemunha5 = None
                    if request.POST['testemunha6']:
                        testemunha6 = request.POST['testemunha6']
                    else:
                        testemunha6 = None
                    if request.POST['testemunha7']:
                        testemunha7 = request.POST['testemunha7']
                    else:
                        testemunha7 = None
                    if request.POST['testemunha8']:
                        testemunha8 = request.POST['testemunha8']
                    else:
                        testemunha8 = None
                    if request.POST['testemunha9']:
                        testemunha9 = request.POST['testemunha9']
                    else:
                        testemunha9 = None
                    if request.POST['testemunha10']:
                        testemunha10 = request.POST['testemunha10']
                    else:
                        testemunha10 = None

                    testemunhas = Testemunhas(
                        id_tarefa=id_tarefa,
                        testemunha1=testemunha1,
                        testemunha2=testemunha2,
                        testemunha3=testemunha3,
                        testemunha4=testemunha4,
                        testemunha5=testemunha5,
                        testemunha6=testemunha6,
                        testemunha7=testemunha7,
                        testemunha8=testemunha8,
                        testemunha9=testemunha9,
                        testemunha10=testemunha10
                    )
                    testemunhas.save()

                    autor1 = request.POST['autor1']
                    if request.POST['autor2']:
                        autor2 = request.POST['autor2']
                    else:
                        autor2 = None
                    if request.POST['autor3']:
                        autor3 = request.POST['autor3']
                    else:
                        autor3 = None
                    if request.POST['autor4']:
                        autor4 = request.POST['autor4']
                    else:
                        autor4 = None
                    if request.POST['autor5']:
                        autor5 = request.POST['autor5']
                    else:
                        autor5 = None
                    if request.POST['autor6']:
                        autor6 = request.POST['autor6']
                    else:
                        autor6 = None
                    if request.POST['autor7']:
                        autor7 = request.POST['autor7']
                    else:
                        autor7 = None
                    if request.POST['autor8']:
                        autor8 = request.POST['autor8']
                    else:
                        autor8 = None
                    if request.POST['autor9']:
                        autor9 = request.POST['autor9']
                    else:
                        autor9 = None
                    if request.POST['autor10']:
                        autor10 = request.POST['autor10']
                    else:
                        autor10 = None

                    autor = Autor(
                        id_tarefa=id_tarefa,
                        autor1=autor1,
                        autor2=autor2,
                        autor3=autor3,
                        autor4=autor4,
                        autor5=autor5,
                        autor6=autor6,
                        autor7=autor7,
                        autor8=autor8,
                        autor9=autor9,
                        autor10=autor10
                    )
                    autor.save()

                    reu1 = request.POST['reu1']
                    if request.POST['reu2']:
                        reu2 = request.POST['reu2']
                    else:
                        reu2 = None
                    if request.POST['reu3']:
                        reu3 = request.POST['reu3']
                    else:
                        reu3 = None
                    if request.POST['reu4']:
                        reu4 = request.POST['reu4']
                    else:
                        reu4 = None
                    if request.POST['reu5']:
                        reu5 = request.POST['reu5']
                    else:
                        reu5 = None
                    if request.POST['reu6']:
                        reu6 = request.POST['reu6']
                    else:
                        reu6 = None
                    if request.POST['reu7']:
                        reu7 = request.POST['reu7']
                    else:
                        reu7 = None
                    if request.POST['reu8']:
                        reu8 = request.POST['reu8']
                    else:
                        reu8 = None
                    if request.POST['reu9']:
                        reu9 = request.POST['reu9']
                    else:
                        reu9 = None
                    if request.POST['reu10']:
                        reu10 = request.POST['reu10']
                    else:
                        reu10 = None

                    reu = Reu(
                        id_tarefa=id_tarefa,
                        reu1=reu1,
                        reu2=reu2,
                        reu3=reu3,
                        reu4=reu4,
                        reu5=reu5,
                        reu6=reu6,
                        reu7=reu7,
                        reu8=reu8,
                        reu9=reu9,
                        reu10=reu10
                    )
                    reu.save()
                else:
                    print("Não há jurídico")
            else:
                juridico.escritorio = request.POST['escritorio']
                juridico.escritorio_advogado = request.POST['escritorio_advogado']
                juridico.resumo_processo = request.POST['id_resumo_processo']
                juridico.numero_processo = request.POST['numero_processo']
                juridico.autor_assistente = request.POST['autor_assistente']
                juridico.autor_advogado = request.POST['autor_advogado']
                juridico.reu_assistente = request.POST['reu_assistente']
                juridico.reu_advogado = request.POST['reu_advogado']
                aux = request.POST['prazo_interno']
                juridico.prazo_interno = aux[6:] + "-" + aux[3:5] + "-" + aux[:2]
                juridico.observacoes = request.POST['id_observacoes']
                juridico.valor_estimado = request.POST['valor_estimado']
                juridico.valor_causa = request.POST['valor_causa']
                juridico.valor_acordo = request.POST['valor_acordo']
                juridico.perito = request.POST['perito']
                juridico.preposto = request.POST['preposto']
                juridico.jBloco = request.POST['jBloco']
                juridico.jUnidade = request.POST['jUnidade']

                juridico.save()

                testemunhas.testemunha1 = request.POST['testemunha1']
                if request.POST['testemunha2']:
                    testemunhas.testemunha2 = request.POST['testemunha2']
                else:
                    testemunhas.testemunha2 = None
                if request.POST['testemunha3']:
                    testemunhas.testemunha3 = request.POST['testemunha3']
                else:
                    testemunhas.testemunha3 = None
                if request.POST['testemunha4']:
                    testemunhas.testemunha4 = request.POST['testemunha4']
                else:
                    testemunhas.testemunha4 = None
                if request.POST['testemunha5']:
                    testemunhas.testemunha5 = request.POST['testemunha5']
                else:
                    testemunhas.testemunha5 = None
                if request.POST['testemunha6']:
                    testemunhas.testemunha6 = request.POST['testemunha6']
                else:
                    testemunhas.testemunha6 = None
                if request.POST['testemunha7']:
                    testemunhas.testemunha7 = request.POST['testemunha7']
                else:
                    testemunhas.testemunha7 = None
                if request.POST['testemunha8']:
                    testemunhas.testemunha8 = request.POST['testemunha8']
                else:
                    testemunhas.testemunha8 = None
                if request.POST['testemunha9']:
                    testemunhas.testemunha9 = request.POST['testemunha9']
                else:
                    testemunhas.testemunha9 = None
                if request.POST['testemunha10']:
                    testemunhas.testemunha10 = request.POST['testemunha10']
                else:
                    testemunhas.testemunha10 = None
                testemunhas.save()

                autor.autor1 = request.POST['autor1']
                if request.POST['autor2']:
                    autor.autor2 = request.POST['autor2']
                else:
                    autor.autor2 = None
                if request.POST['autor3']:
                    autor.autor3 = request.POST['autor3']
                else:
                    autor.autor3 = None
                if request.POST['autor4']:
                    autor.autor4 = request.POST['autor4']
                else:
                    autor.autor4 = None
                if request.POST['autor5']:
                    autor.autor5 = request.POST['autor5']
                else:
                    autor.autor5 = None
                if request.POST['autor6']:
                    autor.autor6 = request.POST['autor6']
                else:
                    autor.autor6 = None
                if request.POST['autor7']:
                    autor.autor7 = request.POST['autor7']
                else:
                    autor.autor7 = None
                if request.POST['autor8']:
                    autor.autor8 = request.POST['autor8']
                else:
                    autor.autor8 = None
                if request.POST['autor9']:
                    autor.autor9 = request.POST['autor9']
                else:
                    autor.autor9 = None
                if request.POST['autor10']:
                    autor.autor10 = request.POST['autor10']
                else:
                    autor.autor10 = None
                autor.save()

                reu.reu1 = request.POST['reu1']
                if request.POST['reu2']:
                    reu.reu2 = request.POST['reu2']
                else:
                    reu.reu2 = None
                if request.POST['reu3']:
                    reu.reu3 = request.POST['reu3']
                else:
                    reu.reu3 = None
                if request.POST['reu4']:
                    reu.reu4 = request.POST['reu4']
                else:
                    reu.reu4 = None
                if request.POST['reu5']:
                    reu.reu5 = request.POST['reu5']
                else:
                    reu.reu5 = None
                if request.POST['reu6']:
                    reu.reu6 = request.POST['reu6']
                else:
                    reu.reu6 = None
                if request.POST['reu7']:
                    reu.reu7 = request.POST['reu7']
                else:
                    reu.reu7 = None
                if request.POST['reu8']:
                    reu.reu8 = request.POST['reu8']
                else:
                    reu.reu8 = None
                if request.POST['reu9']:
                    reu.reu9 = request.POST['reu9']
                else:
                    reu.reu9 = None
                if request.POST['reu10']:
                    reu.reu10 = request.POST['reu10']
                else:
                    reu.reu10 = None
                reu.save()

            messages.success(request, 'A tarefa foi atualizada com sucesso!', extra_tags='success')
            return HttpResponseRedirect(reverse('Tarefa:editar', args=(id,)))

        else:
            print(FormTarefa.errors)

            messages.success(request, 'Falha ao atualizar a tarefa', extra_tags='danger')
            return HttpResponseRedirect(reverse('Tarefa:editar', args=(id,)))
    
    context = {
        "form" : form, 
        "tarefa" : tarefa, 
        "usuario" : usuario, 
        "executores_form": executores_form,
        "etapas" : etapas,
        "subetapas" : subetapas,
        "r5w2h" : r5w2h,
        "retrospectiva" : retrospectiva,
        "solicitacao" : solicitacao,
        "medicao_terceiros" : medicao_terceiros,
        "medicao_terceiros_form" : medicao_terceiros_form,

        "locacao" : locacao,
        "filhos" : filhos,
        "executoresFilhos" : executoresFilhos,

        "filhosAFazer" : filhosAFazer,
        "filhosFazendo" : filhosFazendo,
        "filhosFeito" : filhosFeito,

        "solicitacao_form" : solicitacao_form,
        "locacao_form" : locacao_form,
        "problema" : problema,
        "juridico" : juridico,
        'tarefas' : tarefas,
        "testemunhas" : testemunhas,
        "juridico_form" : juridico_form,
        "testemunhas_form" : testemunhas_form,
        "autor" : autor,
        "reu" : reu,
        "autor_form" : autor_form,
        "reu_form" : reu_form,

    }

    return render(request, 'editarTarefas.html', context)

@login_required(login_url=urls.getUrlSubdominio())
def cadastrarFilhos(request, id):
    usuario = get_user(request.user)

    tarefa = get_object_or_404(Tarefa, pk=id, id_empresa=usuario.id_empresa)
    tarefa_form = TarefaForms(request, instance=tarefa)
    form = TarefaForms(request)
    executores_form = ExecutorForms(request)

    retrospectiva = ""
    r5w2h = ""

    try:
        locacao = get_object_or_404(Locacao, id_tarefa=tarefa.id_locacao)
        locacao_form = LocacaoForms(instance=locacao)
    except:
        locacao = ""
        locacao_form = LocacaoForms()

    if request.method == 'POST':
        form = TarefaForms(request, request.POST)
        executores_form = ExecutorForms(request, request.POST)
        print(form.is_valid())
        # Tarefas #
        # if form.is_valid():
        calendario = None
        data_calendario = None
    
        if request.POST['calendario'] == '1':
            calendario = 1
            data_calendario = "{}-00:00".format(request.POST['data_calendario'])

        if form.cleaned_data['processo_relacionado'].id_processo == 63:
            new_tarefa = Tarefa(
                id_empresa = usuario.id_empresa,
                descri = form.cleaned_data['descri'],
                id_centro_custo = form.cleaned_data['id_centro_custo'],
                prioridade = form.cleaned_data['prioridade'],
                stat = form.cleaned_data['stat'],
                id_tamanho = form.cleaned_data['id_tamanho'],
                porcentagem = form.cleaned_data['porcentagem'],
                prazo = form.cleaned_data['prazo'],
                data_ini = form.cleaned_data['data_ini'],
                data_real = form.cleaned_data['data_real'],
                data_fim = form.cleaned_data['data_fim'],
                data_finalizacao = form.cleaned_data['data_finalizacao'],
                pendente_por = form.cleaned_data['pendente_por'],
                status_pendencia = form.cleaned_data['status_pendencia'],
                historico = form.cleaned_data['historico'],
                id_departamento = form.cleaned_data['id_departamento'],
                responsavel = form.cleaned_data['responsavel'],
                autoridade = form.cleaned_data['autoridade'],
                processo_relacionado = form.cleaned_data['processo_relacionado'],
                id_pessoa = form.cleaned_data['id_pessoa'],
                last_update = datetime.now(),
                id_update = form.cleaned_data['id_update'],
                checado = form.cleaned_data['checado'],
                etapa = form.cleaned_data['etapa'],
                subetapa = form.cleaned_data['subetapa'],
                retrospec = form.cleaned_data['retrospec'],
                calendario = calendario,
                data_calendario = data_calendario,
                id_filho = tarefa.id_filho,
                id_status = form.cleaned_data['id_status'],
            )
            new_tarefa.save()

            id_locacao = tarefa.id_locacao

            new_tarefa.id_locacao = id_locacao
            new_tarefa.save()

            # Executores #
            if executores_form.is_valid():
                new_executores = Executor(
                    executor1 = executores_form.cleaned_data['executor1'],
                    porcento1 = executores_form.cleaned_data['porcento1'],
                    executor2 = executores_form.cleaned_data['executor2'],
                    porcento2 = executores_form.cleaned_data['porcento2'],
                    executor3 = executores_form.cleaned_data['executor3'],
                    porcento3 = executores_form.cleaned_data['porcento3'],
                    executor4 = executores_form.cleaned_data['executor4'],
                    porcento4 = executores_form.cleaned_data['porcento4'],
                    executor5 = executores_form.cleaned_data['executor5'],
                    porcento5 = executores_form.cleaned_data['porcento5'],
                    executor6 = executores_form.cleaned_data['executor6'],
                    porcento6 = executores_form.cleaned_data['porcento6'],
                    executor7 = executores_form.cleaned_data['executor7'],
                    porcento7 = executores_form.cleaned_data['porcento7'],
                    executor8 = executores_form.cleaned_data['executor8'],
                    porcento8 = executores_form.cleaned_data['porcento8'],
                    executor9 = executores_form.cleaned_data['executor9'],
                    porcento9 = executores_form.cleaned_data['porcento9'],
                    executor10 = executores_form.cleaned_data['executor10'],
                    porcento10 = executores_form.cleaned_data['porcento10'],
                    id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                )
                new_executores.save()
            else:
                context = {
                    'form' : form,
                    'executores_form' : executores_form,
                    'usuario' : usuario
                }
                messages.success(request, 'Falha ao cadastrar a tarefa!', extra_tags='danger')
                return render(request, 'cadastrarTarefas.html', context)
        else:
            tarefa.id_filho = tarefa.id_tarefa
            tarefa.id_status = 0
            tarefa.save()
            
            new_tarefa = Tarefa(
                id_empresa = usuario.id_empresa,
                descri = form.cleaned_data['descri'],
                id_centro_custo = form.cleaned_data['id_centro_custo'],
                prioridade = form.cleaned_data['prioridade'],
                stat = form.cleaned_data['stat'],
                id_tamanho = form.cleaned_data['id_tamanho'],
                porcentagem = form.cleaned_data['porcentagem'],
                prazo = form.cleaned_data['prazo'],
                data_ini = form.cleaned_data['data_ini'],
                data_real = form.cleaned_data['data_real'],
                data_fim = form.cleaned_data['data_fim'],
                data_finalizacao = form.cleaned_data['data_finalizacao'],
                data_finalizacao_sat = form.cleaned_data['data_finalizacao_sat'],
                pendente_por = form.cleaned_data['pendente_por'],
                status_pendencia = form.cleaned_data['status_pendencia'],
                historico = form.cleaned_data['historico'],
                id_departamento = form.cleaned_data['id_departamento'],
                responsavel = form.cleaned_data['responsavel'],
                autoridade = form.cleaned_data['autoridade'],
                #dpto_correto = form.cleaned_data['dpto_correto'],
                processo_relacionado = form.cleaned_data['processo_relacionado'],
                id_pessoa = form.cleaned_data['id_pessoa'],
                last_update = datetime.now(),
                id_update = form.cleaned_data['id_update'],
                #predecessor_1 = form.cleaned_data['predecessor_1'],
                #predecessor_2 = form.cleaned_data['predecessor_2'],
                #predecessor_3 = form.cleaned_data['predecessor_3'],
                #anexo1 = form.cleaned_data['anexo1'],
                #anexo2 = form.cleaned_data['anexo2'],
                #anexo3 = form.cleaned_data['anexo3'],
                #anexo4 = form.cleaned_data['anexo4'],
                checado = form.cleaned_data['checado'],
                etapa = form.cleaned_data['etapa'],
                subetapa = form.cleaned_data['subetapa'],
                retrospec = form.cleaned_data['retrospec'],
                calendario = calendario,
                id_filho = tarefa.id_tarefa,
                id_status = 1,
                data_calendario = data_calendario,
            )
            new_tarefa.save()

            # Executores #
            if executores_form.is_valid():
                new_executores = Executor(
                    executor1 = executores_form.cleaned_data['executor1'],
                    porcento1 = executores_form.cleaned_data['porcento1'],
                    executor2 = executores_form.cleaned_data['executor2'],
                    porcento2 = executores_form.cleaned_data['porcento2'],
                    executor3 = executores_form.cleaned_data['executor3'],
                    porcento3 = executores_form.cleaned_data['porcento3'],
                    executor4 = executores_form.cleaned_data['executor4'],
                    porcento4 = executores_form.cleaned_data['porcento4'],
                    executor5 = executores_form.cleaned_data['executor5'],
                    porcento5 = executores_form.cleaned_data['porcento5'],
                    executor6 = executores_form.cleaned_data['executor6'],
                    porcento6 = executores_form.cleaned_data['porcento6'],
                    executor7 = executores_form.cleaned_data['executor7'],
                    porcento7 = executores_form.cleaned_data['porcento7'],
                    executor8 = executores_form.cleaned_data['executor8'],
                    porcento8 = executores_form.cleaned_data['porcento8'],
                    executor9 = executores_form.cleaned_data['executor9'],
                    porcento9 = executores_form.cleaned_data['porcento9'],
                    executor10 = executores_form.cleaned_data['executor10'],
                    porcento10 = executores_form.cleaned_data['porcento10'],
                    id_tarefa = Tarefa.objects.get(pk=new_tarefa.id_tarefa),
                )

                new_executores.save()
            else:
                context = {
                    'form' : form,
                    'executores_form' : executores_form,
                    'usuario' : usuario
                }
                messages.success(request, 'Falha ao cadastrar a tarefa!', extra_tags='danger')
                return HttpResponseRedirect(reverse('Tarefa:filhos', args=(tarefa.id_tarefa,)))

        if (retrospectiva == ""):
            if (request.POST['classificacao'] != ""):
                id_tarefa = Tarefa.objects.get(pk = new_tarefa.id_tarefa)
                descricao = request.POST['classificacao']
                stats = request.POST['rStat']
                rResponsavel = request.POST['id_responsavel']

                id_pessoa_objects = Pessoa.objects.all().filter(id_user=request.user.id)
                id_update = id_pessoa_objects[0]
                id_pessoa_objects = Pessoa.objects.all().filter(id_pessoa=rResponsavel)
                rResponsavel = id_pessoa_objects[0]
                nome_responsavel = id_pessoa_objects[0].nome
                last_update = datetime.now()

                retrospectiva = Retrospectiva(id_tarefa=id_tarefa, descricao=descricao, stats=stats, finalizado=0, id_update=id_update, last_update=last_update, id_responsavel=rResponsavel, nome_responsavel=nome_responsavel)
                retrospectiva.save()
                # print("Retrospectiva cadastrada!")
            else:
                print("Não há retrospectiva!")
        else:
            retrospectiva = get_object_or_404(Retrospectiva, id_tarefa=id)
            retrospectiva.id_tarefa = Tarefa.objects.get(pk = new_tarefa.id_tarefa)
            retrospectiva.descricao = request.POST['classificacao']
            retrospectiva.stats = request.POST['rStat']
            retrospectiva.finalizado = request.POST['finalizado']
            rResponsavel = request.POST['id_responsavel']
            
            id_pessoa_objects = Pessoa.objects.all().filter(id_pessoa=rResponsavel)
            rResponsavel = id_pessoa_objects[0]
            retrospectiva.id_responsavel = rResponsavel
            retrospectiva.nome_responsavel = id_pessoa_objects[0].nome
            
            retrospectiva.save()

        if (r5w2h == ""):
            if (request.POST['rWhat'] != ""):
                id_tarefa = Tarefa.objects.get(pk = new_tarefa.id_tarefa)
                rWhat = request.POST['rWhat']
                rWhy = request.POST['rWhy']
                rWhere = request.POST['rWhere']
                rWhen = request.POST['rWhen']
                rWho = request.POST['rWho']
                rHow = request.POST['rHow']
                rHowMuch = request.POST['rHowMuch']

                id_pessoa_objects = Pessoa.objects.all().filter(id_user=request.user.id)
                id_update = id_pessoa_objects[0]
                last_update = datetime.now()

                r5w2h = R5w2h(id_tarefa=id_tarefa, rWhat=rWhat, rWhy=rWhy, rWhere=rWhere, rWhen=rWhen, rWho=rWho, rHow=rHow, rHowMuch=rHowMuch, id_update=id_update, last_update=last_update)
                r5w2h.save()
                # print("5w2h cadastrado!")
            else:
                print("Não há 5w2h!")
        else:
            r5w2h = get_object_or_404(R5w2h, id_tarefa=id)
            r5w2h.id_tarefa = Tarefa.objects.get(pk = new_tarefa.id_tarefa)
            r5w2h.rWhat = request.POST['rWhat']
            r5w2h.rWhy = request.POST['rWhy']
            r5w2h.rWhere = request.POST['rWhere']
            r5w2h.rWhen = request.POST['rWhen']
            r5w2h.rWho = request.POST['rWho']
            r5w2h.rHow = request.POST['rHow']
            r5w2h.rHowMuch = request.POST['rHowMuch']
            
            r5w2h.save()

        messages.success(request, 'A tarefa foi cadastrada com sucesso!', extra_tags='success')
        return HttpResponseRedirect(reverse('Tarefa:editar', args=(new_tarefa.id_tarefa,)))

    context = {
        'tarefa' : tarefa,
        'form' : form,
        'usuario' : usuario,
        'tarefa_form' : tarefa_form,
        'executores_form' : executores_form,
        "r5w2h" : r5w2h,
        "retrospectiva" : retrospectiva,
        "locacao" : locacao,
        "locacao_form" : locacao_form
    }

    return render(request, 'cadastrarFilhos.html', context)

def getEtapa(request, id):
    if request.method == 'GET' and request.is_ajax():
        etapas = Etapas.objects.filter(id_cc=id)

    data = serializers.serialize('json', list(etapas))
    return HttpResponse(json.dumps(data))

def getSubEtapa(request, id):
    if request.method == 'GET' and request.is_ajax():
        subetapas = SubEtapas.objects.filter(id_etapa=id)

    data = serializers.serialize('json', list(subetapas))
    return HttpResponse(json.dumps(data))

def getR5w2h(request, id):
    if request.method == 'GET':
        r5w2h = R5w2h.objects.filter(id_tarefa=id)

    data = serializers.serialize('json', list(r5w2h))
    return HttpResponse(json.dumps(data))

def getRetrospectiva(request, id):
    if request.method == 'GET':
        retrospectivas = Retrospectiva.objects.filter(id_tarefa=id)

    data = serializers.serialize('json', list(retrospectivas))
    return HttpResponse(json.dumps(data))

def getProblemas(request, id):
    if request.method == 'GET':
        try:
            solicitacao = Solicitacao.objects.get(id_tarefa=id)
            problemas = Problema.objects.filter(id_solicitacao=solicitacao.id_solicitacao)
        except:
            problemas = ""

    data = serializers.serialize('json', list(problemas))
    return HttpResponse(json.dumps(data))

# Importação e Exportação de tarefas
def importarTarefas(request):
    usuario = get_user(request.user)
    #Buscando ID do usuário atual
    id_pessoa_objects = Pessoa.objects.all().filter(id_user=request.user.id)
    id_pessoa = id_pessoa_objects[0]

    tarefas = []

    if request.method == 'POST':
        arquivo = request.FILES['planilha']

        #Salva os arquivos no diretório MEDIA_ROOT do projeto
        fs = FileSystemStorage()
        filename = fs.save(arquivo.name, arquivo)
        uploaded_file_url = fs.path(filename)

        #Faz a leitura do arquivo Excel
        abrir_planilha = xlrd.open_workbook(uploaded_file_url)

        #Lê os dados da primeira planilha da pasta Excel
        dados = abrir_planilha.sheet_by_index(0)

        #Se a linha for difente de zero ele vai printar todas abaixo da primeira linha
        for linha in range(dados.nrows):
            if linha !=0:
                id_tarefa = dados.row(linha)[0].value
                descricao = dados.row(linha)[1].value
                prioridade = int(dados.row(linha)[2].value)
                centro_custo = dados.row(linha)[3].value
                status = dados.row(linha)[4].value
                tamanho = dados.row(linha)[5].value
                porcentagem = int(dados.row(linha)[6].value)
                prazo = int(dados.row(linha)[7].value)
                data_inicial = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[8].value), abrir_planilha.datemode)
                data_real = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[9].value), abrir_planilha.datemode)
                data_finalizacao = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[10].value), abrir_planilha.datemode)
                data_fim = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[11].value), abrir_planilha.datemode)
                executor1 = dados.row(linha)[12].value
                porcento1 = dados.row(linha)[13].value
                executor2 = dados.row(linha)[14].value
                porcento2 = dados.row(linha)[15].value
                executor3 = dados.row(linha)[16].value
                porcento3 = dados.row(linha)[17].value
                executor4 = dados.row(linha)[18].value
                porcento4 = dados.row(linha)[19].value
                executor5 = dados.row(linha)[20].value
                porcento5 = dados.row(linha)[21].value
                executor6 = dados.row(linha)[22].value
                porcento6 = dados.row(linha)[23].value
                executor7 = dados.row(linha)[24].value
                porcento7 = dados.row(linha)[25].value
                executor8 = dados.row(linha)[26].value
                porcento8 = dados.row(linha)[27].value
                executor9 = dados.row(linha)[28].value
                porcento9 = dados.row(linha)[29].value
                executor10 = dados.row(linha)[30].value
                porcento10 = dados.row(linha)[31].value
                impedimento = dados.row(linha)[32].value
                status_pendencia = dados.row(linha)[33].value
                historico = dados.row(linha)[34].value
                departamento = dados.row(linha)[35].value
                responsavel = dados.row(linha)[36].value
                autoridade = dados.row(linha)[37].value
                etapa = dados.row(linha)[38].value
                subetapa = dados.row(linha)[39].value
                processo = dados.row(linha)[40].value
                predecessor1 = dados.row(linha)[41].value
                predecessor2 = dados.row(linha)[42].value
                predecessor3 = dados.row(linha)[43].value
                checado = dados.row(linha)[44].value

                try:
                    #Se o campo ID tarefa na planilha for igual a nada ele irá criar uma nova tarefa
                    if id_tarefa == '':
                        #Instancia de objetos das chaves estrangeiras
                        centro_custo_objects = CentroCusto.objects.filter(centrocusto=centro_custo)
                        id_centro_custo = centro_custo_objects[0]

                        tamanho_objects = Tamanho.objects.all().filter(descricao=tamanho)
                        id_tamanho = tamanho_objects[0]

                        departamento_objects = Departamento.objects.all().filter(departamento=departamento)
                        id_departamento = departamento_objects[0]

                        processo_relacionado_objects = Processos.objects.all().filter(processo=processo)
                        processo_relacionado = processo_relacionado_objects[0]

                        autoridade_objects = Pessoa.objects.get(nome=autoridade)
                        autoridade = autoridade_objects

                        responsavel_objects = Pessoa.objects.get(nome=responsavel)
                        responsavel = responsavel_objects

                        #Se não houver algum dos objetos abaixo na tarefa, será inserido no banco o valor nulo
                        try:
                            etapa_objects = Etapas.objects.all().filter(etapa=etapa)
                            etapa = etapa_objects[0]
                        except:
                            etapa = None

                        try:
                            subetapa_objects = SubEtapas.objects.all().filter(subetapa=subetapa)
                            subetapa = subetapa_objects[0]
                        except:
                            subetapa = None

                        try:
                            checado_objects = Pessoa.objects.get(nome=checado)
                            checado = checado_objects
                        except:
                            checado = None
                        try:
                            pendente_por_objects = Pessoa.objects.get(nome=impedimento)
                            pendente_por = pendente_por_objects
                        except:
                            pendente_por = None
                            
                        #Se não houver predecessor o valor inserido no banco será nulo
                        if predecessor1 == '':
                            predecessor1 = None
                        if predecessor2 == '':
                            predecessor2 = None
                        if predecessor3 == '':
                            predecessor3 = None
                        
                        # Corrige possível erro de cálculo entre data inicial e final esperada da tarefa conforme prazo
                        data_finalizacao = data_inicial + timedelta(days = prazo)

                        # Verifica se status é A fazer ou Fazendo e calcula data fim conforme início e prazo
                        if status == 'A fazer' or status == 'Fazendo':
                            data_fim = data_finalizacao

                        tarefa = Tarefa(id_empresa=usuario.id_empresa, descri=descricao, stat=status.capitalize(), prioridade=prioridade, data_ini=data_inicial, data_real=data_real, data_finalizacao=data_finalizacao, 
                            data_fim=data_fim, prazo=prazo, id_tamanho=id_tamanho, porcentagem=porcentagem, id_departamento=id_departamento, id_centro_custo=id_centro_custo, autoridade=autoridade,
                            responsavel=responsavel, historico=historico, status_pendencia=status_pendencia, processo_relacionado=processo_relacionado,
                            predecessor_1= predecessor1, predecessor_2=predecessor2, predecessor_3=predecessor3, etapa=etapa, subetapa=subetapa, pendente_por=pendente_por,
                            checado=checado, id_pessoa=id_pessoa, id_update=id_pessoa, last_update=datetime.now()
                        )

                        tarefa.save()
                        
                        #Se o campo executor estiver vazio irá inserir no banco o valor nulo
                        executor1 = Pessoa.objects.get(nome=executor1)

                        if executor2 == '':
                            executor2 = None
                        else:
                            executor2 = Pessoa.objects.get(nome=executor2)
                        if executor3 == '':
                            executor3 = None
                        else:
                            executor3 = Pessoa.objects.get(nome=executor3)
                        if executor4 == '':
                            executor4 = None
                        else:
                            executor4 = Pessoa.objects.get(nome=executor4)
                        if executor5 == '':
                            executor5 = None
                        else:
                            executor5 = Pessoa.objects.get(nome=executor5)
                        if executor6 == '':
                            executor6 = None
                        else:
                            executor6 = Pessoa.objects.get(nome=executor6)
                        if executor7 == '':
                            executor7 = None
                        else:
                            executor7 = Pessoa.objects.get(nome=executor7)
                        if executor8 == '':
                            executor8 = None
                        else:
                            executor8 = Pessoa.objects.get(nome=executor8)
                        if executor9 == '':
                            executor9 = None
                        else:
                            executor9 = Pessoa.objects.get(nome=executor9)
                        if executor10 == '':
                            executor10 = None
                        else:
                            executor10 = Pessoa.objects.get(nome=executor10)

                        #Se o valor de porcentagem por executor não existir ele irá inserir no banco o valor nulo
                        if porcento2 == '':
                            porcento2 = None
                        if porcento3 == '':
                            porcento3 = None
                        if porcento4 == '':
                            porcento4 = None
                        if porcento5 == '':
                            porcento5 = None
                        if porcento6 == '':
                            porcento6 = None
                        if porcento7 == '':
                            porcento7 = None
                        if porcento8 == '':
                            porcento8 = None
                        if porcento9 == '':
                            porcento9 = None
                        if porcento10 == '':
                            porcento10 = None

                        executor = Executor(
                            executor1 = executor1,
                            porcento1 = porcento1,
                            executor2 = executor2,
                            porcento2 = porcento2,
                            executor3 = executor3,
                            porcento3 = porcento3,
                            executor4 = executor4,
                            porcento4 = porcento4,
                            executor5 = executor5,
                            porcento5 = porcento5,
                            executor6 = executor6,
                            porcento6 = porcento6,
                            executor7 = executor7,
                            porcento7 = porcento7,
                            executor8 = executor8,
                            porcento8 = porcento8,
                            executor9 = executor9,
                            porcento9 = porcento9,
                            executor10 = executor10,
                            porcento10 = porcento10,
                            id_tarefa = tarefa,
                        )

                        executor.save()

                        tarefa.result = 'Cadastrada com sucesso'
                        tarefas.append(tarefa)
                except:
                    tarefa = Tarefa(id_tarefa=linha, descri=dados.row(linha)[1].value)
                    tarefa.centro_custo = centro_custo
                    tarefa.departamento = departamento
                    tarefa.porcentagem = porcentagem
                    tarefa.prioridade = prioridade
                    tarefa.result = 'Falha no cadastro'
                    tarefas.append(tarefa)

                try:
                    if id_tarefa != '':
                        id_tarefa = int(id_tarefa)

                        centro_custo_objects = CentroCusto.objects.filter(centrocusto=centro_custo)
                        id_centro_custo = centro_custo_objects[0]

                        tamanho_objects = Tamanho.objects.all().filter(descricao=tamanho)
                        id_tamanho = tamanho_objects[0]

                        departamento_objects = Departamento.objects.all().filter(departamento=departamento)
                        id_departamento = departamento_objects[0]

                        processo_relacionado_objects = Processos.objects.all().filter(processo=processo)
                        processo_relacionado = processo_relacionado_objects[0]

                        autoridade_objects = Pessoa.objects.get(nome=autoridade)
                        autoridade = autoridade_objects

                        responsavel_objects = Pessoa.objects.get(nome=responsavel)
                        responsavel = responsavel_objects
                        
                        try:
                            etapa_objects = Etapas.objects.all().filter(etapa=etapa)
                            etapa = etapa_objects[0]
                        except:
                            etapa = None

                        try:
                            subetapa_objects = SubEtapas.objects.all().filter(subetapa=subetapa)
                            subetapa = subetapa_objects[0]
                        except:
                            subetapa = None

                        try:
                            checado_objects = Pessoa.objects.get(nome=checado)
                            checado = checado_objects
                        except:
                            checado = None
                        try:
                            pendente_por_objects = Pessoa.objects.get(nome=impedimento)
                            pendente_por = pendente_por_objects
                        except:
                            pendente_por = None

                        #Se não houver predecessor o valor inserido no banco será nulo
                        if predecessor1 == '':
                            predecessor1 = None
                        if predecessor2 == '':
                            predecessor2 = None
                        if predecessor3 == '':
                            predecessor3 = None

                        # Verifica se tarefa é A fazer ou Fazendo e calcula data fim real pelo início e prazo
                        if status == 'A fazer' or status == 'Fazendo':
                            data_fim = data_inicial + timedelta(days = prazo)
                        
                        tarefa = Tarefa(id_tarefa=id_tarefa, id_empresa=usuario.id_empresa, descri=descricao, stat=status.capitalize(), prioridade=prioridade, data_ini=data_inicial, data_real=data_real, 
                            data_fim=data_fim, prazo=prazo, id_tamanho=id_tamanho, porcentagem=porcentagem, id_departamento=id_departamento, id_centro_custo=id_centro_custo, autoridade=autoridade,
                            responsavel=responsavel, historico=historico, status_pendencia=status_pendencia,processo_relacionado=processo_relacionado,
                            etapa=etapa, subetapa=subetapa, pendente_por=pendente_por, predecessor_1=predecessor1, predecessor_2=predecessor2,
                            predecessor_3=predecessor3, checado=checado, id_pessoa=id_pessoa, id_update=id_pessoa, last_update=datetime.now()
                        )

                        tarefa.save(update_fields=['id_empresa', 'descri', 'stat', 'prioridade','data_ini', 
                            'data_real', 'data_fim','prazo', 'id_tamanho', 'porcentagem', 'id_departamento',
                            'id_centro_custo', 'autoridade','responsavel', 'historico', 'status_pendencia',
                            'processo_relacionado', 'etapa','subetapa','pendente_por','checado',
                            'predecessor_1', 'predecessor_2', 'predecessor_3','id_pessoa', 'id_update', 'last_update'],force_update=True)
                        

                        #Se o campo executor estiver vazio irá inserir no banco o valor nulo
                        executor1 = Pessoa.objects.get(nome=executor1)

                        if executor2 == '':
                            executor2 = None
                        else:
                            executor2 = Pessoa.objects.get(nome=executor2)
                        if executor3 == '':
                            executor3 = None
                        else:
                            executor3 = Pessoa.objects.get(nome=executor3)
                        if executor4 == '':
                            executor4 = None
                        else:
                            executor4 = Pessoa.objects.get(nome=executor4)
                        if executor5 == '':
                            executor5 = None
                        else:
                            executor5 = Pessoa.objects.get(nome=executor5)
                        if executor6 == '':
                            executor6 = None
                        else:
                            executor6 = Pessoa.objects.get(nome=executor6)
                        if executor7 == '':
                            executor7 = None
                        else:
                            executor7 = Pessoa.objects.get(nome=executor7)
                        if executor8 == '':
                            executor8 = None
                        else:
                            executor8 = Pessoa.objects.get(nome=executor8)
                        if executor9 == '':
                            executor9 = None
                        else:
                            executor9 = Pessoa.objects.get(nome=executor9)
                        if executor10 == '':
                            executor10 = None
                        else:
                            executor10 = Pessoa.objects.get(nome=executor10)

                        if porcento2 == '':
                            porcento2 = None
                        if porcento3 == '':
                            porcento3 = None
                        if porcento4 == '':
                            porcento4 = None
                        if porcento5 == '':
                            porcento5 = None
                        if porcento6 == '':
                            porcento6 = None
                        if porcento7 == '':
                            porcento7 = None
                        if porcento8 == '':
                            porcento8 = None
                        if porcento9 == '':
                            porcento9 = None
                        if porcento10 == '':
                            porcento10 = None

                        executor = Executor.objects.get(id_tarefa=id_tarefa)
                        executor.executor1 = executor1
                        executor.porcento1 = porcento1
                        executor.executor2 = executor2
                        executor.porcento2 = porcento2
                        executor.executor3 = executor3
                        executor.porcento3 = porcento3
                        executor.executor4 = executor4
                        executor.porcento4 = porcento4
                        executor.executor5 = executor5
                        executor.porcento5 = porcento5
                        executor.executor6 = executor6
                        executor.porcento6 = porcento6
                        executor.executor7 = executor7
                        executor.porcento7 = porcento7
                        executor.executor8 = executor8
                        executor.porcento8 = porcento8
                        executor.executor9 = executor9
                        executor.porcento9 = porcento9
                        executor.executor10 = executor10
                        executor.porcento10 = porcento10

                        executor.save(update_fields= ['executor1','porcento1','executor2','porcento2','executor3',
                            'porcento3','executor4','porcento4','executor5','porcento5','executor6','porcento6',
                            'executor7','porcento7','executor8','porcento8','executor9','porcento9','executor10',
                            'porcento10','id_tarefa'])

                        tarefa.result = 'Atualizada com sucesso'
                        tarefas.append(tarefa)
                except:
                    tarefa = Tarefa(id_tarefa=linha, descri=dados.row(linha)[1].value)
                    tarefa.centro_custo = centro_custo
                    tarefa.departamento = departamento
                    tarefa.porcentagem = porcentagem
                    tarefa.prioridade = prioridade
                    tarefa.result = 'Falha na atualização'
                    tarefas.append(tarefa)

        os.remove(uploaded_file_url)
    
    context = {
        "usuario": usuario,
        "tarefas" : tarefas
    }
    

    return render(request, "importarTarefas.html", context)

def exportarTarefa(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    data = datetime.now().strftime('%Y-%m-%d')

    model = 'ExportarTarefa'

    filename = f'MyScrum Tarefas {data} ({usuario.nome}).xls'
    
    queryset = ExportarTarefas.objects.all().extra(where=[filtrosWhere['WHERE']]).order_by('prioridade').values_list(
        'id_tarefa',
        'descri',
        'prioridade',
        'centro_custo',
        'stat',
        'tamanho',
        'porcentagem',
        'prazo',
        'data_ini',
        'data_real',
        'data_finalizacao',
        'data_fim',
        'executor1',
        'porcento1',
        'executor2',
        'porcento2',
        'executor3',
        'porcento3',
        'executor4',
        'porcento4',
        'executor5',
        'porcento5',
        'executor6',
        'porcento6',
        'executor7',
        'porcento7',
        'executor8',
        'porcento8',
        'executor9',
        'porcento9',
        'executor10',
        'porcento10',
        'pendente_por',
        'status_pendencia',
        'historico',
        'departamento',
        'responsavel',
        'autoridade',
        'etapa',
        'subetapa',
        'processo_relacionado',
        'predecessor_1',
        'predecessor_2',
        'predecessor_3',
        'checado',

    )

    columns = (
        'id_tarefa',
        'descrição',
        'prioridade',
        'centro de custo',
        'status',
        'tamanho',
        'porcentagem',
        'prazo',
        'data incio',
        'data real',
        'data fim',
        'data fim real',
        'executor1',
        'porcento1',
        'executor2',
        'porcento2',
        'executor3',
        'porcento3',
        'executor4',
        'porcento4',
        'executor5',
        'porcento5',
        'executor6',
        'porcento6',
        'executor7',
        'porcento7',
        'executor8',
        'porcento8',
        'executor9',
        'porcento9',
        'executor10',
        'porcento10',
        'impedimento',
        'status pendencia',
        'historico',
        'departamento',
        'responsavel',
        'autoridade',
        'etapa',
        'subetapa',
        'processo relacionado',
        'predecessor 1',
        'predecessor 2',
        'predecessor 3',
        'checado',
    )

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    default_style = xlwt.XFStyle()

    rows = queryset
    for row, rowdata in enumerate(rows):
        row_num += 1
        for col, val in enumerate(rowdata):
            ws.write(row_num, col, val, default_style)

    wb.save(response)
    return response

def importarMaeFilho(request):
    usuario = get_user(request.user)
    #Buscando ID do usuário atual
    id_pessoa_objects = Pessoa.objects.all().filter(id_user=request.user.id)
    id_pessoa = id_pessoa_objects[0]

    tarefas = []

    if request.method == 'POST':
        arquivo = request.FILES['planilha']

        #Salva os arquivos no diretório MEDIA_ROOT do projeto
        fs = FileSystemStorage()
        filename = fs.save(arquivo.name, arquivo)
        uploaded_file_url = fs.path(filename)

        #Faz a leitura do arquivo Excel
        abrir_planilha = xlrd.open_workbook(uploaded_file_url)

        #Lê os dados da primeira planilha da pasta Excel
        dados = abrir_planilha.sheet_by_index(0)

        #Se a linha for difente de zero ele vai printar todas abaixo da primeira linha
        for linha in range(dados.nrows):
            if linha !=0:
                id_tarefa = dados.row(linha)[0].value
                id_status = dados.row(linha)[1].value
                id_filho = dados.row(linha)[2].value
                descricao = dados.row(linha)[3].value
                prioridade = int(dados.row(linha)[4].value)
                centro_custo = dados.row(linha)[5].value
                status = dados.row(linha)[6].value
                tamanho = dados.row(linha)[7].value
                porcentagem = int(dados.row(linha)[8].value)
                prazo = int(dados.row(linha)[9].value)
                data_inicial = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[10].value), abrir_planilha.datemode)
                data_real = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[11].value), abrir_planilha.datemode)
                data_finalizacao = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[12].value), abrir_planilha.datemode)
                data_fim = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[13].value), abrir_planilha.datemode)
                executor1 = dados.row(linha)[14].value
                porcento1 = dados.row(linha)[15].value
                executor2 = dados.row(linha)[16].value
                porcento2 = dados.row(linha)[17].value
                executor3 = dados.row(linha)[18].value
                porcento3 = dados.row(linha)[19].value
                executor4 = dados.row(linha)[20].value
                porcento4 = dados.row(linha)[21].value
                executor5 = dados.row(linha)[22].value
                porcento5 = dados.row(linha)[23].value
                executor6 = dados.row(linha)[24].value
                porcento6 = dados.row(linha)[25].value
                executor7 = dados.row(linha)[26].value
                porcento7 = dados.row(linha)[27].value
                executor8 = dados.row(linha)[28].value
                porcento8 = dados.row(linha)[29].value
                executor9 = dados.row(linha)[30].value
                porcento9 = dados.row(linha)[31].value
                executor10 = dados.row(linha)[32].value
                porcento10 = dados.row(linha)[33].value
                impedimento = dados.row(linha)[34].value
                status_pendencia = dados.row(linha)[35].value
                historico = dados.row(linha)[36].value
                departamento = dados.row(linha)[37].value
                responsavel = dados.row(linha)[38].value
                autoridade = dados.row(linha)[39].value
                etapa = dados.row(linha)[40].value
                subetapa = dados.row(linha)[41].value
                processo = dados.row(linha)[42].value
                predecessor1 = dados.row(linha)[43].value
                predecessor2 = dados.row(linha)[44].value
                predecessor3 = dados.row(linha)[45].value
                checado = dados.row(linha)[46].value

                if id_status == 'Mãe':
                    id_status = 0
                else:
                    id_status = 1

                try:
                    #Se o campo ID tarefa na planilha for igual a nada ele irá criar uma nova tarefa
                    if id_tarefa == '':
                        #Instancia de objetos das chaves estrangeiras
                        centro_custo_objects = CentroCusto.objects.filter(centrocusto=centro_custo)
                        id_centro_custo = centro_custo_objects[0]

                        tamanho_objects = Tamanho.objects.all().filter(descricao=tamanho)
                        id_tamanho = tamanho_objects[0]

                        departamento_objects = Departamento.objects.all().filter(departamento=departamento)
                        id_departamento = departamento_objects[0]

                        processo_relacionado_objects = Processos.objects.all().filter(processo=processo)
                        processo_relacionado = processo_relacionado_objects[0]

                        autoridade_objects = Pessoa.objects.get(nome=autoridade)
                        autoridade = autoridade_objects

                        responsavel_objects = Pessoa.objects.get(nome=responsavel)
                        responsavel = responsavel_objects

                        #Se não houver algum dos objetos abaixo na tarefa, será inserido no banco o valor nulo
                        try:
                            etapa_objects = Etapas.objects.all().filter(etapa=etapa)
                            etapa = etapa_objects[0]
                        except:
                            etapa = None

                        try:
                            subetapa_objects = SubEtapas.objects.all().filter(subetapa=subetapa)
                            subetapa = subetapa_objects[0]
                        except:
                            subetapa = None

                        try:
                            checado_objects = Pessoa.objects.get(nome=checado)
                            checado = checado_objects
                        except:
                            checado = None
                        try:
                            pendente_por_objects = Pessoa.objects.get(nome=impedimento)
                            pendente_por = pendente_por_objects
                        except:
                            pendente_por = None
                            
                        #Se não houver predecessor o valor inserido no banco será nulo
                        if predecessor1 == '':
                            predecessor1 = None
                        if predecessor2 == '':
                            predecessor2 = None
                        if predecessor3 == '':
                            predecessor3 = None
                        
                        # Corrige possível erro de cálculo entre data inicial e final esperada da tarefa conforme prazo
                        data_finalizacao = data_inicial + timedelta(days = prazo)

                        # Verifica se status é A fazer ou Fazendo e calcula data fim conforme início e prazo
                        if status == 'A fazer' or status == 'Fazendo':
                            data_fim = data_finalizacao

                        tarefa = Tarefa(id_empresa=usuario.id_empresa, id_status=id_status, id_filho=id_filho, descri=descricao, stat=status.capitalize(), prioridade=prioridade, data_ini=data_inicial, data_real=data_real, data_finalizacao=data_finalizacao, 
                            data_fim=data_fim, prazo=prazo, id_tamanho=id_tamanho, porcentagem=porcentagem, id_departamento=id_departamento, id_centro_custo=id_centro_custo, autoridade=autoridade,
                            responsavel=responsavel, historico=historico, status_pendencia=status_pendencia, processo_relacionado=processo_relacionado,
                            predecessor_1= predecessor1, predecessor_2=predecessor2, predecessor_3=predecessor3, etapa=etapa, subetapa=subetapa, pendente_por=pendente_por,
                            checado=checado, id_pessoa=id_pessoa, id_update=id_pessoa, last_update=datetime.now()
                        )

                        tarefa.save()
                        
                        #Se o campo executor estiver vazio irá inserir no banco o valor nulo
                        executor1 = Pessoa.objects.get(nome=executor1)

                        if executor2 == '':
                            executor2 = None
                        else:
                            executor2 = Pessoa.objects.get(nome=executor2)
                        if executor3 == '':
                            executor3 = None
                        else:
                            executor3 = Pessoa.objects.get(nome=executor3)
                        if executor4 == '':
                            executor4 = None
                        else:
                            executor4 = Pessoa.objects.get(nome=executor4)
                        if executor5 == '':
                            executor5 = None
                        else:
                            executor5 = Pessoa.objects.get(nome=executor5)
                        if executor6 == '':
                            executor6 = None
                        else:
                            executor6 = Pessoa.objects.get(nome=executor6)
                        if executor7 == '':
                            executor7 = None
                        else:
                            executor7 = Pessoa.objects.get(nome=executor7)
                        if executor8 == '':
                            executor8 = None
                        else:
                            executor8 = Pessoa.objects.get(nome=executor8)
                        if executor9 == '':
                            executor9 = None
                        else:
                            executor9 = Pessoa.objects.get(nome=executor9)
                        if executor10 == '':
                            executor10 = None
                        else:
                            executor10 = Pessoa.objects.get(nome=executor10)

                        #Se o valor de porcentagem por executor não existir ele irá inserir no banco o valor nulo
                        if porcento2 == '':
                            porcento2 = None
                        if porcento3 == '':
                            porcento3 = None
                        if porcento4 == '':
                            porcento4 = None
                        if porcento5 == '':
                            porcento5 = None
                        if porcento6 == '':
                            porcento6 = None
                        if porcento7 == '':
                            porcento7 = None
                        if porcento8 == '':
                            porcento8 = None
                        if porcento9 == '':
                            porcento9 = None
                        if porcento10 == '':
                            porcento10 = None

                        executor = Executor(
                            executor1 = executor1,
                            porcento1 = porcento1,
                            executor2 = executor2,
                            porcento2 = porcento2,
                            executor3 = executor3,
                            porcento3 = porcento3,
                            executor4 = executor4,
                            porcento4 = porcento4,
                            executor5 = executor5,
                            porcento5 = porcento5,
                            executor6 = executor6,
                            porcento6 = porcento6,
                            executor7 = executor7,
                            porcento7 = porcento7,
                            executor8 = executor8,
                            porcento8 = porcento8,
                            executor9 = executor9,
                            porcento9 = porcento9,
                            executor10 = executor10,
                            porcento10 = porcento10,
                            id_tarefa = tarefa,
                        )

                        executor.save()

                        tarefa.result = 'Cadastrada com sucesso'
                        tarefas.append(tarefa)
                except:
                    tarefa = Tarefa(id_tarefa=linha, descri=dados.row(linha)[1].value)
                    tarefa.centro_custo = centro_custo
                    tarefa.departamento = departamento
                    tarefa.porcentagem = porcentagem
                    tarefa.prioridade = prioridade
                    tarefa.result = 'Falha no cadastro'
                    tarefas.append(tarefa)

                try:
                    if id_tarefa != '':
                        id_tarefa = int(id_tarefa)

                        centro_custo_objects = CentroCusto.objects.filter(centrocusto=centro_custo)
                        id_centro_custo = centro_custo_objects[0]

                        tamanho_objects = Tamanho.objects.all().filter(descricao=tamanho)
                        id_tamanho = tamanho_objects[0]

                        departamento_objects = Departamento.objects.all().filter(departamento=departamento)
                        id_departamento = departamento_objects[0]

                        processo_relacionado_objects = Processos.objects.all().filter(processo=processo)
                        processo_relacionado = processo_relacionado_objects[0]

                        autoridade_objects = Pessoa.objects.get(nome=autoridade)
                        autoridade = autoridade_objects

                        responsavel_objects = Pessoa.objects.get(nome=responsavel)
                        responsavel = responsavel_objects
                        
                        try:
                            etapa_objects = Etapas.objects.all().filter(etapa=etapa)
                            etapa = etapa_objects[0]
                        except:
                            etapa = None

                        try:
                            subetapa_objects = SubEtapas.objects.all().filter(subetapa=subetapa)
                            subetapa = subetapa_objects[0]
                        except:
                            subetapa = None

                        try:
                            checado_objects = Pessoa.objects.get(nome=checado)
                            checado = checado_objects
                        except:
                            checado = None
                        try:
                            pendente_por_objects = Pessoa.objects.get(nome=impedimento)
                            pendente_por = pendente_por_objects
                        except:
                            pendente_por = None

                        #Se não houver predecessor o valor inserido no banco será nulo
                        if predecessor1 == '':
                            predecessor1 = None
                        if predecessor2 == '':
                            predecessor2 = None
                        if predecessor3 == '':
                            predecessor3 = None

                        # Verifica se tarefa é A fazer ou Fazendo e calcula data fim real pelo início e prazo
                        if status == 'A fazer' or status == 'Fazendo':
                            data_fim = data_inicial + timedelta(days = prazo)
                        
                        tarefa = Tarefa(id_tarefa=id_tarefa, id_status=id_status, id_filho=id_filho, id_empresa=usuario.id_empresa, descri=descricao, stat=status.capitalize(), prioridade=prioridade, data_ini=data_inicial, data_real=data_real, 
                            data_fim=data_fim, prazo=prazo, id_tamanho=id_tamanho, porcentagem=porcentagem, id_departamento=id_departamento, id_centro_custo=id_centro_custo, autoridade=autoridade,
                            responsavel=responsavel, historico=historico, status_pendencia=status_pendencia,processo_relacionado=processo_relacionado,
                            etapa=etapa, subetapa=subetapa, pendente_por=pendente_por, predecessor_1=predecessor1, predecessor_2=predecessor2,
                            predecessor_3=predecessor3, checado=checado, id_pessoa=id_pessoa, id_update=id_pessoa, last_update=datetime.now()
                        )

                        tarefa.save(update_fields=['id_empresa', 'id_status', 'id_filho', 'descri', 'stat', 'prioridade','data_ini', 
                            'data_real', 'data_fim','prazo', 'id_tamanho', 'porcentagem', 'id_departamento',
                            'id_centro_custo', 'autoridade','responsavel', 'historico', 'status_pendencia',
                            'processo_relacionado', 'etapa','subetapa','pendente_por','checado',
                            'predecessor_1', 'predecessor_2', 'predecessor_3','id_pessoa', 'id_update', 'last_update'],force_update=True)
                        

                        #Se o campo executor estiver vazio irá inserir no banco o valor nulo
                        executor1 = Pessoa.objects.get(nome=executor1)

                        if executor2 == '':
                            executor2 = None
                        else:
                            executor2 = Pessoa.objects.get(nome=executor2)
                        if executor3 == '':
                            executor3 = None
                        else:
                            executor3 = Pessoa.objects.get(nome=executor3)
                        if executor4 == '':
                            executor4 = None
                        else:
                            executor4 = Pessoa.objects.get(nome=executor4)
                        if executor5 == '':
                            executor5 = None
                        else:
                            executor5 = Pessoa.objects.get(nome=executor5)
                        if executor6 == '':
                            executor6 = None
                        else:
                            executor6 = Pessoa.objects.get(nome=executor6)
                        if executor7 == '':
                            executor7 = None
                        else:
                            executor7 = Pessoa.objects.get(nome=executor7)
                        if executor8 == '':
                            executor8 = None
                        else:
                            executor8 = Pessoa.objects.get(nome=executor8)
                        if executor9 == '':
                            executor9 = None
                        else:
                            executor9 = Pessoa.objects.get(nome=executor9)
                        if executor10 == '':
                            executor10 = None
                        else:
                            executor10 = Pessoa.objects.get(nome=executor10)

                        if porcento2 == '':
                            porcento2 = None
                        if porcento3 == '':
                            porcento3 = None
                        if porcento4 == '':
                            porcento4 = None
                        if porcento5 == '':
                            porcento5 = None
                        if porcento6 == '':
                            porcento6 = None
                        if porcento7 == '':
                            porcento7 = None
                        if porcento8 == '':
                            porcento8 = None
                        if porcento9 == '':
                            porcento9 = None
                        if porcento10 == '':
                            porcento10 = None

                        executor = Executor.objects.get(id_tarefa=id_tarefa)
                        executor.executor1 = executor1
                        executor.porcento1 = porcento1
                        executor.executor2 = executor2
                        executor.porcento2 = porcento2
                        executor.executor3 = executor3
                        executor.porcento3 = porcento3
                        executor.executor4 = executor4
                        executor.porcento4 = porcento4
                        executor.executor5 = executor5
                        executor.porcento5 = porcento5
                        executor.executor6 = executor6
                        executor.porcento6 = porcento6
                        executor.executor7 = executor7
                        executor.porcento7 = porcento7
                        executor.executor8 = executor8
                        executor.porcento8 = porcento8
                        executor.executor9 = executor9
                        executor.porcento9 = porcento9
                        executor.executor10 = executor10
                        executor.porcento10 = porcento10

                        executor.save(update_fields= ['executor1','porcento1','executor2','porcento2','executor3',
                            'porcento3','executor4','porcento4','executor5','porcento5','executor6','porcento6',
                            'executor7','porcento7','executor8','porcento8','executor9','porcento9','executor10',
                            'porcento10','id_tarefa'])

                        tarefa.result = 'Atualizada com sucesso'
                        tarefas.append(tarefa)
                except:
                    tarefa = Tarefa(id_tarefa=linha, descri=dados.row(linha)[1].value)
                    tarefa.centro_custo = centro_custo
                    tarefa.departamento = departamento
                    tarefa.porcentagem = porcentagem
                    tarefa.prioridade = prioridade
                    tarefa.result = 'Falha na atualização'
                    tarefas.append(tarefa)

        os.remove(uploaded_file_url)
    
    context = {
        "usuario": usuario,
        "tarefas" : tarefas
    }
    

    return render(request, "importarTarefas.html", context)

def exportarMaeFilho(request):
    usuario = get_user(request.user)

    WHERE = f"""
    id_filho = """ + request.GET.get('tarefa-mae') + """ AND

    CASE 
        WHEN stat != 'Teste'
            THEN 
                id_tarefa != 0
    END
    """

    data = datetime.now().strftime('%Y-%m-%d')

    model = 'ExportarTarefa'

    filename = f'MyScrum Mãe-Filho {data} ({usuario.nome}).xls'
    
    queryset = ExportarTarefas.objects.all().extra(where=[WHERE]).order_by('id_status').values_list(
        'id_tarefa',
        'id_status',
        'id_filho',
        'descri',
        'prioridade',
        'centro_custo',
        'stat',
        'tamanho',
        'porcentagem',
        'prazo',
        'data_ini',
        'data_real',
        'data_finalizacao',
        'data_fim',
        'executor1',
        'porcento1',
        'executor2',
        'porcento2',
        'executor3',
        'porcento3',
        'executor4',
        'porcento4',
        'executor5',
        'porcento5',
        'executor6',
        'porcento6',
        'executor7',
        'porcento7',
        'executor8',
        'porcento8',
        'executor9',
        'porcento9',
        'executor10',
        'porcento10',
        'pendente_por',
        'status_pendencia',
        'historico',
        'departamento',
        'responsavel',
        'autoridade',
        'etapa',
        'subetapa',
        'processo_relacionado',
        'predecessor_1',
        'predecessor_2',
        'predecessor_3',
        'checado'
    )

    columns = (
        'id_tarefa',
        'tipo tarefa',
        'tarefa mãe',
        'descrição',
        'prioridade',
        'centro de custo',
        'status',
        'tamanho',
        'porcentagem',
        'prazo',
        'data incio',
        'data real',
        'data fim',
        'data fim real',
        'executor1',
        'porcento1',
        'executor2',
        'porcento2',
        'executor3',
        'porcento3',
        'executor4',
        'porcento4',
        'executor5',
        'porcento5',
        'executor6',
        'porcento6',
        'executor7',
        'porcento7',
        'executor8',
        'porcento8',
        'executor9',
        'porcento9',
        'executor10',
        'porcento10',
        'impedimento',
        'status pendencia',
        'historico',
        'departamento',
        'responsavel',
        'autoridade',
        'etapa',
        'subetapa',
        'processo relacionado',
        'predecessor 1',
        'predecessor 2',
        'predecessor 3',
        'checado'
    )

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    default_style = xlwt.XFStyle()

    listaTarefas = []
    for tarefa in queryset:
        cList = list(tarefa)
        if cList[1] == 0:
            cList[1] = "Mãe"  
        else:
            cList[1] = "Filho"
        listaTarefas.append(cList)

    rows = listaTarefas

    for row, rowdata in enumerate(rows):
        row_num += 1
        for col, val in enumerate(rowdata):
            ws.write(row_num, col, val, default_style)

    wb.save(response)
    return response

# Função que gera os filtros baseado no form do request 
def gerarFiltros(request, usuario):
    tarefas = []
    filtros = {}
    filtrosHierarquia = ""
    filtrosStatus = ""
    filtrosCC = ""
    filtrosEtapa = ""
    filtrosSubEtapa = ""
    filtrosDPTO = ""
    filtrosProcesso = ""
    filtrosAutoridade = ""
    filtrosResponsavel = ""
    filtrosPessoa = ""
    filtrosExecutor = ""
    filtrosImpedimento = ""
    filtros5w2h = ""

    #################--------------------##########################
    ################# Filtro de Datas #############################
    # Se existir valor na data usamos o valor escolhido, se não usamos o valor do periodo atual
    if request.GET.get('start') != None and request.GET.get('end') != None :
        data_inicio = datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date()
        data_fim = datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date()
        
        filtros['start'] = data_inicio.strftime("%d/%m/%Y")
        filtros['end'] = data_fim.strftime("%d/%m/%Y")

    else:
        hoje = date.today()
        if hoje.month != 12:
            data_fim = date(hoje.year, hoje.month+1, 1 ) - timedelta(days=1)
        else:
            data_fim = date(hoje.year+1, 1, 1 ) - timedelta(days=1)
        data_inicio = date(hoje.year, hoje.month, 1 )

        filtros['start'] = data_inicio.strftime("%d/%m/%Y")
        filtros['end'] = data_fim.strftime("%d/%m/%Y")
    ################# Filtro de Datas #############################
    #################--------------------##########################

    #################--------------------##########################
    ################# Filtro de Status ############################
    # Monta a lista com os status da tarefa selecionado
    status = []
    
    if 'A fazer' in request.GET.getlist('status'):
        status.append('A fazer')
    
    if 'Fazendo' in request.GET.getlist('status'):
        status.append('Fazendo')

    if 'Feito' in request.GET.getlist('status'):
        status.append('Feito')

    if 'Cancelado' in request.GET.getlist('status'):
        status.append('Cancelado')
    
    filtros['status'] = status
    
    if len(status) != 0:
        status = str(status).replace('[','(').replace(']',')')
    else:
        status = "('A fazer', 'Fazendo', 'Feito')"

    filtrosStatus = f''' stat in {status} AND '''
    ################# Filtro de Status ############################
    #################--------------------##########################

    #################--------------------##########################
    ################# Filtro de Centro de custo ##################
    # Se o campo centrocusto não estiver vazio filtra tarefas baseada no centrocusto de custo escolhido
    if request.GET.get('centrocusto') != None and request.GET.get('centrocusto') != 'Centros de custo':
        filtros['centrocusto'] = CentroCusto.objects.get(id_centro_custo=request.GET.get('centrocusto')).centrocusto
        centro_custo = CentroCusto.objects.get(id_centro_custo=request.GET.get('centrocusto')).centrocusto
        filtrosCC = f''' centro_custo = '{centro_custo}' AND '''
    ################# Filtro de Centro de custo ##################
    #################--------------------##########################

    #################--------------------##########################
    ################# Filtro de Etapa    ##########################
    # Se o campo processo não estiver vazio filtra tarefas baseada no departamento escolhido
    if request.GET.get('etapa') != None and request.GET.get('etapa') != '0':
        filtros['etapa'] = Etapas.objects.get(id_etapa=request.GET.get('etapa')).etapa
        etapa = Etapas.objects.get(id_etapa=request.GET.get('etapa')).etapa
        filtrosEtapa = f''' etapa = '{etapa}' AND '''
    ################# Filtro de Etapa ######################
    #################--------------------##########################

    #################--------------------##########################
    
    ################# Filtro de SubEtapa    ##########################
    # Se o campo processo não estiver vazio filtra tarefas baseada no departamento escolhido
    if request.GET.get('subetapa') != None and request.GET.get('subetapa') != '0':
        filtros['subetapa'] = SubEtapas.objects.get(id_sub_etapas=request.GET.get('subetapa')).sub_etapa
        subetapa = SubEtapas.objects.get(id_sub_etapas=request.GET.get('subetapa')).sub_etapa
        filtrosSubEtapa = f''' subetapa = '{subetapa}' AND '''
    ################# Filtro de SubEtapa ######################
    #################--------------------##########################

    #################--------------------##########################
    ################# Filtro de Departamento ######################
    departamentos = request.GET.getlist('departamento')
    if len(departamentos) != 0 :
        filtros['departamento'] = departamentos
        departamentos = str(departamentos).replace('[','(').replace(']',')')
        filtrosDPTO = f''' departamento in {departamentos} AND '''
    ################# Filtro de Departamento ######################
    #################--------------------##########################

    #################--------------------##########################
    ################# Filtro de Processo ##########################
    processos = request.GET.getlist('processo')
    if len(processos):
        filtros['processo'] = processos
        processos = str(processos).replace('[','(').replace(']',')')
        filtrosProcesso = f''' processo_relacionado in {processos} AND '''
    ################# Filtro de Processo ##########################
    #################--------------------##########################

    #################--------------------############################
    ################# Filtro de Autoridade ##########################
    autoridades = request.GET.getlist('autoridade')
    if len(autoridades):
        filtros['autoridade'] = autoridades
        autoridades = str(autoridades).replace('[','(').replace(']',')')
        filtrosAutoridade = f''' autoridade in {autoridades} AND '''
    ################# Filtro de Autoridade ##########################
    #################--------------------############################

    #################--------------------############################
    ################# Filtro de Responsavel #########################
    responsaveis = request.GET.getlist('responsavel')
    if len(responsaveis):
        filtros['responsavel'] = responsaveis
        responsaveis = str(responsaveis).replace('[','(').replace(']',')')
        filtrosResponsavel = f''' responsavel in {responsaveis} AND '''
    ################# Filtro de Responsavel #########################
    #################--------------------############################

    #################--------------------############################
    ################# Filtro de Pessoas #############################
    pessoas = request.GET.getlist('pessoa')
    if len(pessoas):
        filtros['pessoa'] = pessoas
        pessoas = str(pessoas).replace('[','(').replace(']',')')
        filtrosPessoa = f''' (autoridade in {pessoas} OR 
        responsavel in {pessoas} OR
        pendente_por in {pessoas} OR
        checado in {pessoas} OR
        executor1 in {pessoas} OR
        executor2 in {pessoas} OR
        executor3 in {pessoas} OR
        executor4 in {pessoas} OR
        executor5 in {pessoas} OR
        executor6 in {pessoas} OR
        executor7 in {pessoas} OR
        executor8 in {pessoas} OR
        executor9 in {pessoas} OR
        executor10 in {pessoas}) AND'''
    ################# Filtro de Pessoas #############################
    #################--------------------############################

    #################--------------------############################
    ################# Filtro de Executor ############################
    executores = request.GET.getlist('executor')
    if len(executores):
        filtros['executor'] = executores
        executores = str(executores).replace('[','(').replace(']',')')
        filtrosExecutor = f''' (executor1 in {executores} OR
        executor2 in {executores} OR
        executor3 in {executores} OR
        executor4 in {executores} OR
        executor5 in {executores} OR
        executor6 in {executores} OR
        executor7 in {executores} OR
        executor8 in {executores} OR
        executor9 in {executores} OR
        executor10 in {executores}) AND'''
    ################# Filtro de Executor ############################
    #################--------------------############################
    
    #################--------------------############################
    ################# Filtro de Impedimento #########################
    impedimentos = request.GET.getlist('impedimento')
    if len(impedimentos):
        filtros['impedimento'] = impedimentos
        impedimentos = str(impedimentos).replace('[','(').replace(']',')')
        filtrosImpedimento = f''' pendente_por in {impedimentos} AND '''
    ################# Filtro de Impedimento #########################
    #################--------------------############################

    #################--------------------############################
    #################   Filtro de 5W2H   ############################
    if request.GET.get('r5w2h') != None and request.GET.get('r5w2h') != '-------':
        r5w2hT = request.GET.getlist('r5w2h')
        if len(r5w2hT):
            filtros['r5w2h'] = r5w2hT
            r5w2hT = str(r5w2hT).replace('[','(').replace(']',')')
            filtros5w2h = f''' r5w2hT in {r5w2hT} AND '''
    else:
        r5w2hT = ""
    #################   Filtro de 5W2H   ############################
    #################--------------------############################

    #################--------------------##########################
    ################# Filtro de Hierarquia #########################
    vinculos = Vinculos.objects.all().filter(id_usuario=usuario)
    filtrosHierarquia = ""
    vinculosCC = ['valores','para tupla']
    vinculosDPTO = ['valores', 'para tupla']

    # Passando de vinculo em vinculo para coletar o id_cc e id_dpto
    for vinculo in vinculos:
        try:
            vinculosDPTO.append(vinculo.id_dpto.departamento)
        except:
            print('sem vinculos com departamento')

        try:
            vinculosCC.append(vinculo.id_cc.centrocusto)
        except:
            print('sem vinculos com centro de custo')

    if usuario.adm == 0: # Usuario Basico - Acesso apenas para tarefas que contenham seu nome + vinculos
        # Transformando as listas de vinculos em tuplas para entrarem no WHERE no seguinte padrão ('id','id')
        vinculosDPTO = tuple(vinculosDPTO)
        vinculosCC = tuple(vinculosCC)

        filtrosHierarquia = f'''(autoridade = '{usuario.nome}' OR
        responsavel = '{usuario.nome}' OR
        checado = '{usuario.nome}' OR
        pendente_por = '{usuario.nome}' OR
        departamento in {vinculosDPTO} OR
        centro_custo in {vinculosCC} OR
        '{usuario.nome}' in (executor1, executor2, executor3, executor4, executor5, executor6, executor7, executor8, executor9, executor10)) AND '''
    elif usuario.adm == 1: # Administrador - Acesso a todas as tarefas
        filtrosHierarquia = ""
    elif usuario.adm == 2: # Lider - Acesso as tarefas com seu nome ou seu departamento + vinculos
        vinculosDPTO.append(usuario.id_departamento.departamento)

        # Transformando as listas de vinculos em tuplas para entrarem no WHERE no seguinte padrão ('id','id')
        vinculosDPTO = tuple(vinculosDPTO)
        vinculosCC = tuple(vinculosCC)

        filtrosHierarquia = f'''(autoridade = '{usuario.nome}' OR
        responsavel = '{usuario.nome}' OR
        checado = '{usuario.nome}' OR
        pendente_por = '{usuario.nome}' OR
        departamento in {vinculosDPTO} OR
        centro_custo in {vinculosCC} OR
        '{usuario.nome}' in (executor1, executor2, executor3, executor4, executor5, executor6, executor7, executor8, executor9, executor10)) AND '''
    elif usuario.adm == 3: # Gerente -  Acesso as tarefas com seu nome ou seu centro de custo + vinculos
        vinculosCC.append(usuario.id_centrocusto.centrocusto)

        # Transformando as listas de vinculos em tuplas para entrarem no WHERE no seguinte padrão ('id','id')
        vinculosDPTO = tuple(vinculosDPTO)
        vinculosCC = tuple(vinculosCC)

        filtrosHierarquia = f'''(autoridade = '{usuario.nome}' OR
        responsavel = '{usuario.nome}' OR
        checado = '{usuario.nome}' OR
        pendente_por = '{usuario.nome}' OR
        departamento in {vinculosDPTO} OR
        centro_custo in {vinculosCC} OR
        '{usuario.nome}' in (executor1, executor2, executor3, executor4, executor5, executor6, executor7, executor8, executor9, executor10)) AND '''
    ################# Filtro de Hierarquia ##########################
    #################--------------------############################s

    # is_staff = 0, Usuario = tem acesso apenas as tarefas onde contem o seu nome
    # is_staff = 1, Administrador = tem acesso a todas Tarefas
    # is_staff = 2, Lider = tem acessso as tarefas com seu nome e as tarefas do seu departamento
    # is_staff = 3, Gestor = tem acesso as tarefas com sue nome e as tarefas do seu centro custo

    WHERE = f"""
    {filtrosHierarquia}
    {filtrosStatus}
    {filtrosCC}
    {filtrosEtapa}
    {filtrosSubEtapa}
    {filtrosDPTO}
    {filtrosProcesso}
    {filtrosAutoridade}
    {filtrosResponsavel}
    {filtrosPessoa}
    {filtrosExecutor}
    {filtrosImpedimento}
    {filtros5w2h}

    CASE 
        WHEN stat = 'A fazer' and id_empresa={usuario.id_empresa}
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim < '{data_inicio}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Feito' and id_empresa={usuario.id_empresa}
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Cancelado' and id_empresa={usuario.id_empresa}
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Fazendo' and id_empresa={usuario.id_empresa}
            THEN
                id_tarefa != 0
    END
    """
    print(WHERE)

    retorno = {
        'filtros' : filtros,
        'WHERE' : WHERE,
        'r5w2hT' : r5w2hT,
        'status' : status
    }

    return retorno

def importarSolicitacao(request):
    usuario = get_user(request.user)
    #Buscando ID do usuário atual
    id_pessoa_objects = Pessoa.objects.all().filter(id_user=request.user.id)
    id_pessoa = id_pessoa_objects[0]

    solicitacoes = []

    if request.method == 'POST':
        arquivo = request.FILES['planilha']

        #Salva os arquivos no diretório MEDIA_ROOT do projeto
        fs = FileSystemStorage()
        filename = fs.save(arquivo.name, arquivo)
        uploaded_file_url = fs.path(filename)

        #Faz a leitura do arquivo Excel
        abrir_planilha = xlrd.open_workbook(uploaded_file_url)

        #Lê os dados da primeira planilha da pasta Excel
        dados = abrir_planilha.sheet_by_index(0)

        #Se a linha for difente de zero ele vai printar todas abaixo da primeira linha
        for linha in range(dados.nrows):
            if linha !=0:
                id_tarefa = dados.row(linha)[0].value
                descricaoTarefa = dados.row(linha)[1].value
                prioridade = int(dados.row(linha)[2].value)
                centro_custo = dados.row(linha)[3].value
                status = dados.row(linha)[4].value
                tamanho = dados.row(linha)[5].value
                porcentagem = int(dados.row(linha)[6].value)
                prazo = int(dados.row(linha)[7].value)
                data_inicial = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[8].value), abrir_planilha.datemode)
                data_real = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[9].value), abrir_planilha.datemode)
                data_finalizacao = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[10].value), abrir_planilha.datemode)
                data_fim = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[11].value), abrir_planilha.datemode)
                executor1 = dados.row(linha)[12].value
                porcento1 = dados.row(linha)[13].value
                executor2 = dados.row(linha)[14].value
                porcento2 = dados.row(linha)[15].value
                executor3 = dados.row(linha)[16].value
                porcento3 = dados.row(linha)[17].value
                executor4 = dados.row(linha)[18].value
                porcento4 = dados.row(linha)[19].value
                executor5 = dados.row(linha)[20].value
                porcento5 = dados.row(linha)[21].value
                executor6 = dados.row(linha)[22].value
                porcento6 = dados.row(linha)[23].value
                executor7 = dados.row(linha)[24].value
                porcento7 = dados.row(linha)[25].value
                executor8 = dados.row(linha)[26].value
                porcento8 = dados.row(linha)[27].value
                executor9 = dados.row(linha)[28].value
                porcento9 = dados.row(linha)[29].value
                executor10 = dados.row(linha)[30].value
                porcento10 = dados.row(linha)[31].value
                impedimento = dados.row(linha)[32].value
                status_pendencia = dados.row(linha)[33].value
                historicoTarefa = dados.row(linha)[34].value
                departamento = dados.row(linha)[35].value
                responsavel = dados.row(linha)[36].value
                autoridade = dados.row(linha)[37].value
                processo = dados.row(linha)[38].value
                checado = dados.row(linha)[39].value

                empreendimento = dados.row(linha)[40].value
                bloco = dados.row(linha)[41].value
                apto = dados.row(linha)[42].value

                proprietario_nome = dados.row(linha)[43].value
                proprietario_rg = dados.row(linha)[44].value
                proprietario_cpf = dados.row(linha)[45].value
                proprietario_email = dados.row(linha)[46].value
                solicitante_nome = dados.row(linha)[47].value
                solicitante_rg = dados.row(linha)[48].value
                solicitante_cpf = dados.row(linha)[49].value
                solicitante_email = dados.row(linha)[50].value
                telefone1 = dados.row(linha)[51].value
                telefone2 = dados.row(linha)[52].value
                status_processo = dados.row(linha)[53].value
                status_solicitacao = dados.row(linha)[54].value

                if dados.row(linha)[55].value == "":
                    data_entrega = ""
                else:
                    data_entrega = xlrd.xldate.xldate_as_datetime(int(dados.row(linha)[55].value), abrir_planilha.datemode)

                tipo_solicitacao = dados.row(linha)[56].value
                tempo_total = dados.row(linha)[57].value
                satisfacao_avaliacao = dados.row(linha)[58].value
                satisfacao_observacoes = dados.row(linha)[59].value

                finalizado = []
                ambiente = []
                descricao = []
                tipo_reparo = []
                procedencia = []
                historico = []
                estimativa_custo = []
                duracao = []
                material = []

                finalizado.append(dados.row(linha)[60].value)
                ambiente.append(dados.row(linha)[61].value)
                descricao.append(dados.row(linha)[62].value)
                tipo_reparo.append(dados.row(linha)[63].value)
                procedencia.append(dados.row(linha)[64].value)
                historico.append(dados.row(linha)[65].value)
                estimativa_custo.append(dados.row(linha)[66].value)
                duracao.append(dados.row(linha)[67].value)
                material.append(dados.row(linha)[68].value)

                finalizado.append(dados.row(linha)[69].value)
                ambiente.append(dados.row(linha)[70].value)
                descricao.append(dados.row(linha)[71].value)
                tipo_reparo.append(dados.row(linha)[72].value)
                procedencia.append(dados.row(linha)[73].value)
                historico.append(dados.row(linha)[74].value)
                estimativa_custo.append(dados.row(linha)[75].value)
                duracao.append(dados.row(linha)[76].value)
                material.append(dados.row(linha)[77].value)

                finalizado.append(dados.row(linha)[78].value)
                ambiente.append(dados.row(linha)[79].value)
                descricao.append(dados.row(linha)[80].value)
                tipo_reparo.append(dados.row(linha)[81].value)
                procedencia.append(dados.row(linha)[82].value)
                historico.append(dados.row(linha)[83].value)
                estimativa_custo.append(dados.row(linha)[84].value)
                duracao.append(dados.row(linha)[85].value)
                material.append(dados.row(linha)[86].value)

                finalizado.append(dados.row(linha)[87].value)
                ambiente.append(dados.row(linha)[88].value)
                descricao.append(dados.row(linha)[89].value)
                tipo_reparo.append(dados.row(linha)[90].value)
                procedencia.append(dados.row(linha)[91].value)
                historico.append(dados.row(linha)[92].value)
                estimativa_custo.append(dados.row(linha)[93].value)
                duracao.append(dados.row(linha)[94].value)
                material.append(dados.row(linha)[95].value)

                finalizado.append(dados.row(linha)[96].value)
                ambiente.append(dados.row(linha)[97].value)
                descricao.append(dados.row(linha)[98].value)
                tipo_reparo.append(dados.row(linha)[99].value)
                procedencia.append(dados.row(linha)[100].value)
                historico.append(dados.row(linha)[101].value)
                estimativa_custo.append(dados.row(linha)[102].value)
                duracao.append(dados.row(linha)[103].value)
                material.append(dados.row(linha)[104].value)

                finalizado.append(dados.row(linha)[105].value)
                ambiente.append(dados.row(linha)[106].value)
                descricao.append(dados.row(linha)[107].value)
                tipo_reparo.append(dados.row(linha)[108].value)
                procedencia.append(dados.row(linha)[109].value)
                historico.append(dados.row(linha)[110].value)
                estimativa_custo.append(dados.row(linha)[111].value)
                duracao.append(dados.row(linha)[112].value)
                material.append(dados.row(linha)[113].value)

                finalizado.append(dados.row(linha)[114].value)
                ambiente.append(dados.row(linha)[115].value)
                descricao.append(dados.row(linha)[116].value)
                tipo_reparo.append(dados.row(linha)[117].value)
                procedencia.append(dados.row(linha)[118].value)
                historico.append(dados.row(linha)[119].value)
                estimativa_custo.append(dados.row(linha)[120].value)
                duracao.append(dados.row(linha)[121].value)
                material.append(dados.row(linha)[122].value)

                finalizado.append(dados.row(linha)[123].value)
                ambiente.append(dados.row(linha)[124].value)
                descricao.append(dados.row(linha)[125].value)
                tipo_reparo.append(dados.row(linha)[126].value)
                procedencia.append(dados.row(linha)[127].value)
                historico.append(dados.row(linha)[128].value)
                estimativa_custo.append(dados.row(linha)[129].value)
                duracao.append(dados.row(linha)[130].value)
                material.append(dados.row(linha)[131].value)

                finalizado.append(dados.row(linha)[132].value)
                ambiente.append(dados.row(linha)[133].value)
                descricao.append(dados.row(linha)[134].value)
                tipo_reparo.append(dados.row(linha)[135].value)
                procedencia.append(dados.row(linha)[136].value)
                historico.append(dados.row(linha)[137].value)
                estimativa_custo.append(dados.row(linha)[138].value)
                duracao.append(dados.row(linha)[139].value)
                material.append(dados.row(linha)[140].value)

                finalizado.append(dados.row(linha)[141].value)
                ambiente.append(dados.row(linha)[142].value)
                descricao.append(dados.row(linha)[143].value)
                tipo_reparo.append(dados.row(linha)[144].value)
                procedencia.append(dados.row(linha)[145].value)
                historico.append(dados.row(linha)[146].value)
                estimativa_custo.append(dados.row(linha)[147].value)
                duracao.append(dados.row(linha)[148].value)
                material.append(dados.row(linha)[149].value)

                finalizado.append(dados.row(linha)[150].value)
                ambiente.append(dados.row(linha)[151].value)
                descricao.append(dados.row(linha)[152].value)
                tipo_reparo.append(dados.row(linha)[153].value)
                procedencia.append(dados.row(linha)[154].value)
                historico.append(dados.row(linha)[155].value)
                estimativa_custo.append(dados.row(linha)[156].value)
                duracao.append(dados.row(linha)[157].value)
                material.append(dados.row(linha)[158].value)

                finalizado.append(dados.row(linha)[159].value)
                ambiente.append(dados.row(linha)[160].value)
                descricao.append(dados.row(linha)[161].value)
                tipo_reparo.append(dados.row(linha)[162].value)
                procedencia.append(dados.row(linha)[163].value)
                historico.append(dados.row(linha)[164].value)
                estimativa_custo.append(dados.row(linha)[165].value)
                duracao.append(dados.row(linha)[166].value)
                material.append(dados.row(linha)[167].value)

                finalizado.append(dados.row(linha)[168].value)
                ambiente.append(dados.row(linha)[169].value)
                descricao.append(dados.row(linha)[170].value)
                tipo_reparo.append(dados.row(linha)[171].value)
                procedencia.append(dados.row(linha)[172].value)
                historico.append(dados.row(linha)[173].value)
                estimativa_custo.append(dados.row(linha)[174].value)
                duracao.append(dados.row(linha)[175].value)
                material.append(dados.row(linha)[176].value)

                finalizado.append(dados.row(linha)[177].value)
                ambiente.append(dados.row(linha)[178].value)
                descricao.append(dados.row(linha)[179].value)
                tipo_reparo.append(dados.row(linha)[180].value)
                procedencia.append(dados.row(linha)[181].value)
                historico.append(dados.row(linha)[182].value)
                estimativa_custo.append(dados.row(linha)[183].value)
                duracao.append(dados.row(linha)[184].value)
                material.append(dados.row(linha)[185].value)

                finalizado.append(dados.row(linha)[186].value)
                ambiente.append(dados.row(linha)[187].value)
                descricao.append(dados.row(linha)[188].value)
                tipo_reparo.append(dados.row(linha)[189].value)
                procedencia.append(dados.row(linha)[190].value)
                historico.append(dados.row(linha)[191].value)
                estimativa_custo.append(dados.row(linha)[192].value)
                duracao.append(dados.row(linha)[193].value)
                material.append(dados.row(linha)[194].value)

                finalizado.append(dados.row(linha)[195].value)
                ambiente.append(dados.row(linha)[196].value)
                descricao.append(dados.row(linha)[197].value)
                tipo_reparo.append(dados.row(linha)[198].value)
                procedencia.append(dados.row(linha)[199].value)
                historico.append(dados.row(linha)[200].value)
                estimativa_custo.append(dados.row(linha)[201].value)
                duracao.append(dados.row(linha)[202].value)
                material.append(dados.row(linha)[203].value)

                finalizado.append(dados.row(linha)[204].value)
                ambiente.append(dados.row(linha)[205].value)
                descricao.append(dados.row(linha)[206].value)
                tipo_reparo.append(dados.row(linha)[207].value)
                procedencia.append(dados.row(linha)[208].value)
                historico.append(dados.row(linha)[209].value)
                estimativa_custo.append(dados.row(linha)[210].value)
                duracao.append(dados.row(linha)[211].value)
                material.append(dados.row(linha)[212].value)

                finalizado.append(dados.row(linha)[213].value)
                ambiente.append(dados.row(linha)[214].value)
                descricao.append(dados.row(linha)[215].value)
                tipo_reparo.append(dados.row(linha)[216].value)
                procedencia.append(dados.row(linha)[217].value)
                historico.append(dados.row(linha)[218].value)
                estimativa_custo.append(dados.row(linha)[219].value)
                duracao.append(dados.row(linha)[220].value)
                material.append(dados.row(linha)[221].value)

                finalizado.append(dados.row(linha)[222].value)
                ambiente.append(dados.row(linha)[223].value)
                descricao.append(dados.row(linha)[224].value)
                tipo_reparo.append(dados.row(linha)[225].value)
                procedencia.append(dados.row(linha)[226].value)
                historico.append(dados.row(linha)[227].value)
                estimativa_custo.append(dados.row(linha)[228].value)
                duracao.append(dados.row(linha)[229].value)
                material.append(dados.row(linha)[230].value)

                finalizado.append(dados.row(linha)[231].value)
                ambiente.append(dados.row(linha)[232].value)
                descricao.append(dados.row(linha)[233].value)
                tipo_reparo.append(dados.row(linha)[234].value)
                procedencia.append(dados.row(linha)[235].value)
                historico.append(dados.row(linha)[236].value)
                estimativa_custo.append(dados.row(linha)[237].value)
                duracao.append(dados.row(linha)[238].value)
                material.append(dados.row(linha)[239].value)
                
                if bloco == '':
                    bloco = '---'
                if apto == '':
                    apto = None
                if proprietario_nome == '':
                    proprietario_nome = None
                if proprietario_rg == '':
                    proprietario_rg = None
                if proprietario_cpf == '':
                    proprietario_cpf = None
                if proprietario_email == '':
                    proprietario_email = '---'
                if solicitante_nome == '':
                    solicitante_nome = None
                if solicitante_rg == '':
                    solicitante_rg = None
                if solicitante_cpf == '':
                    solicitante_cpf = None
                if solicitante_email == '':
                    solicitante_email = None
                if telefone1 == '':
                    telefone1 = None
                if telefone2 == '':
                    telefone2 = None
                if status_processo == '':
                    status_processo = None
                if status_solicitacao == '':
                    status_solicitacao = None
                if tipo_solicitacao == '':
                    tipo_solicitacao = None
                if data_entrega == '':
                    data_entrega = None
                if satisfacao_avaliacao == '':
                    satisfacao_avaliacao = None
                if satisfacao_observacoes == '':
                    satisfacao_observacoes = None

                try:
                    try:
                        solicitacao = Solicitacao.objects.all().filter(id_tarefa=int(id_tarefa))
                    except:
                        solicitacao = ""
                                        
                    #Se o campo ID tarefa na planilha for igual a nada ele irá criar uma nova tarefa
                    if solicitacao != "":
                        centro_custo_objects = CentroCusto.objects.filter(centrocusto=centro_custo)
                        id_centro_custo = centro_custo_objects[0]

                        tamanho_objects = Tamanho.objects.all().filter(descricao=tamanho)
                        id_tamanho = tamanho_objects[0]

                        departamento_objects = Departamento.objects.all().filter(departamento=departamento)
                        id_departamento = departamento_objects[0]

                        processo_relacionado_objects = Processos.objects.all().filter(processo=processo)
                        processo_relacionado = processo_relacionado_objects[0]

                        autoridade_objects = Pessoa.objects.get(nome=autoridade)
                        autoridade = autoridade_objects

                        responsavel_objects = Pessoa.objects.get(nome=responsavel)
                        responsavel = responsavel_objects

                        #Se não houver algum dos objetos abaixo na tarefa, será inserido no banco o valor nulo
                        try:
                            etapa_objects = Etapas.objects.all().filter(etapa=etapa)
                            etapa = etapa_objects[0]
                        except:
                            etapa = None

                        try:
                            subetapa_objects = SubEtapas.objects.all().filter(subetapa=subetapa)
                            subetapa = subetapa_objects[0]
                        except:
                            subetapa = None

                        try:
                            checado_objects = Pessoa.objects.get(nome=checado)
                            checado = checado_objects
                        except:
                            checado = None

                        try:
                            pendente_por_objects = Pessoa.objects.get(nome=impedimento)
                            pendente_por = pendente_por_objects
                        except:
                            pendente_por = None
                        
                        # Corrige possível erro de cálculo entre data inicial e final esperada da tarefa conforme prazo
                        data_finalizacao = data_inicial + timedelta(days = prazo)
                        
                        # Verifica se status é A fazer ou Fazendo e calcula data fim conforme início e prazo
                        if status == 'A fazer' or status == 'Fazendo':
                            data_fim = data_finalizacao

                        tarefa = Tarefa(id_tarefa=id_tarefa, id_empresa=usuario.id_empresa, descri=descricaoTarefa, stat=status.capitalize(), prioridade=prioridade, data_ini=data_inicial, data_real=data_real, data_finalizacao=data_finalizacao, 
                                data_fim=data_fim, prazo=prazo, id_tamanho=id_tamanho, porcentagem=porcentagem, id_departamento=id_departamento, id_centro_custo=id_centro_custo, autoridade=autoridade,
                                responsavel=responsavel, historico=historicoTarefa, status_pendencia=status_pendencia,processo_relacionado=processo_relacionado,
                                pendente_por=pendente_por, checado=checado, id_pessoa=id_pessoa, id_update=id_pessoa, last_update=datetime.now()
                            )

                        tarefa.save(update_fields=['id_empresa', 'descri', 'stat', 'prioridade','data_ini', 
                            'data_real', 'data_fim','prazo', 'id_tamanho', 'porcentagem', 'id_departamento',
                            'id_centro_custo', 'autoridade','responsavel', 'historico', 'status_pendencia',
                            'processo_relacionado','pendente_por','checado','id_pessoa', 'id_update', 'last_update'],
                            force_update=True)
                        
                        #Se o campo executor estiver vazio irá inserir no banco o valor nulo
                        executor1 = Pessoa.objects.get(nome=executor1)

                        if executor2 == '':
                            executor2 = None
                        else:
                            executor2 = Pessoa.objects.get(nome=executor2)
                        if executor3 == '':
                            executor3 = None
                        else:
                            executor3 = Pessoa.objects.get(nome=executor3)
                        if executor4 == '':
                            executor4 = None
                        else:
                            executor4 = Pessoa.objects.get(nome=executor4)
                        if executor5 == '':
                            executor5 = None
                        else:
                            executor5 = Pessoa.objects.get(nome=executor5)
                        if executor6 == '':
                            executor6 = None
                        else:
                            executor6 = Pessoa.objects.get(nome=executor6)
                        if executor7 == '':
                            executor7 = None
                        else:
                            executor7 = Pessoa.objects.get(nome=executor7)
                        if executor8 == '':
                            executor8 = None
                        else:
                            executor8 = Pessoa.objects.get(nome=executor8)
                        if executor9 == '':
                            executor9 = None
                        else:
                            executor9 = Pessoa.objects.get(nome=executor9)
                        if executor10 == '':
                            executor10 = None
                        else:
                            executor10 = Pessoa.objects.get(nome=executor10)

                        #Se o valor de porcentagem por executor não existir ele irá inserir no banco o valor nulo
                        if porcento2 == '':
                            porcento2 = None
                        if porcento3 == '':
                            porcento3 = None
                        if porcento4 == '':
                            porcento4 = None
                        if porcento5 == '':
                            porcento5 = None
                        if porcento6 == '':
                            porcento6 = None
                        if porcento7 == '':
                            porcento7 = None
                        if porcento8 == '':
                            porcento8 = None
                        if porcento9 == '':
                            porcento9 = None
                        if porcento10 == '':
                            porcento10 = None

                        id_executor = get_object_or_404(Executor, id_tarefa=int(id_tarefa))

                        executor = Executor(id_executor=id_executor.id_executor, id_tarefa=get_object_or_404(Tarefa, id_tarefa=id_tarefa), executor1=executor1, executor2=executor2, executor3=executor3,
                            executor4=executor4,executor5=executor5,executor6=executor6,executor7=executor7,executor8=executor8,
                            executor9=executor9,executor10=executor10, porcento1=porcento1, porcento2=porcento2, porcento3=porcento3,
                            porcento4=porcento4,porcento5=porcento5,porcento6=porcento6,porcento7=porcento7,porcento8=porcento8,
                            porcento9=porcento9,porcento10=porcento10
                        )
                            
                        executor.save(update_fields=[
                            'executor1','porcento1','executor2','porcento2','executor3','porcento3',
                            'executor4','porcento4','executor5','porcento5','executor6','porcento6',
                            'executor7','porcento7','executor8','porcento8','executor9','porcento9',
                            'executor10','porcento10','id_tarefa'],
                            force_update=True
                        )

                        try:
                            solicitacao1 = get_object_or_404(Solicitacao, id_tarefa=int(id_tarefa))
                            solicitacao1.empreendimento=empreendimento
                            solicitacao1.bloco=bloco
                            solicitacao1.unidade=apto
                            solicitacao1.proprietario_nome=proprietario_nome
                            solicitacao1.proprietario_email=proprietario_email
                            solicitacao1.solicitante_nome=solicitante_nome
                            solicitacao1.solicitante_email=solicitante_email
                            solicitacao1.telefone1=telefone1
                            solicitacao1.telefone2=telefone2
                            solicitacao1.status_processo=status_processo
                            solicitacao1.status_solicitacao=status_solicitacao
                            solicitacao1.tipo_solicitacao=tipo_solicitacao
                            solicitacao1.data_entrega=data_entrega
                            solicitacao1.satisfacao_avaliacao=int(satisfacao_avaliacao)
                            solicitacao1.satisfacao_observacoes=satisfacao_observacoes

                            solicitacao1.save()
                        except:
                            None

                        try:
                            problemas = Problema.objects.filter(id_solicitacao=solicitacao1.id_solicitacao)
                            i = 0
                            for problema in problemas:
                                if finalizado[i] == "Sim":
                                    finalizado[i] = 1
                                else:
                                    finalizado[i] = 0
                                problema.finalizado = finalizado[i]
                                problema.ambiente = ambiente[i]
                                problema.descricao_sat = descricao[i]
                                problema.tipo_reparo = tipo_reparo[i]
                                problema.procedencia = procedencia[i]
                                problema.hishistorico_sattorico = historico[i]
                                problema.estimativa_custo = estimativa_custo[i]
                                problema.duracao = duracao[i]
                                problema.material = material[i]
                                problema.save()
                                i += 1
                        except:
                            None

                        solicitacao.id_solicitacao = linha
                        solicitacao.status_solicitacao = dados.row(linha)[1].value
                        solicitacao.proprietario_nome = int(dados.row(linha)[6].value)
                        solicitacao.proprietario_email = int(dados.row(linha)[2].value)
                        solicitacao.solicitante_nome = dados.row(linha)[3].value
                        solicitacao.solicitante_email = dados.row(linha)[35].value
                        solicitacao.telefone1 = dados.row(linha)[4].value
                        solicitacao.result = 'Cadastrada com sucesso'
                        solicitacoes.append(solicitacao)
                    else:
                        centro_custo_objects = CentroCusto.objects.filter(centrocusto=centro_custo)
                        id_centro_custo = centro_custo_objects[0]

                        tamanho_objects = Tamanho.objects.all().filter(descricao=tamanho)
                        id_tamanho = tamanho_objects[0]

                        departamento_objects = Departamento.objects.all().filter(departamento=departamento)
                        id_departamento = departamento_objects[0]

                        processo_relacionado_objects = Processos.objects.all().filter(processo=processo)
                        processo_relacionado = processo_relacionado_objects[0]

                        autoridade_objects = Pessoa.objects.get(nome=autoridade)
                        autoridade = autoridade_objects

                        responsavel_objects = Pessoa.objects.get(nome=responsavel)
                        responsavel = responsavel_objects

                        #Se não houver algum dos objetos abaixo na tarefa, será inserido no banco o valor nulo
                        try:
                            etapa_objects = Etapas.objects.all().filter(etapa=etapa)
                            etapa = etapa_objects[0]
                        except:
                            etapa = None

                        try:
                            subetapa_objects = SubEtapas.objects.all().filter(subetapa=subetapa)
                            subetapa = subetapa_objects[0]
                        except:
                            subetapa = None

                        try:
                            checado_objects = Pessoa.objects.get(nome=checado)
                            checado = checado_objects
                        except:
                            checado = None

                        try:
                            pendente_por_objects = Pessoa.objects.get(nome=impedimento)
                            pendente_por = pendente_por_objects
                        except:
                            pendente_por = None
                        
                        # Corrige possível erro de cálculo entre data inicial e final esperada da tarefa conforme prazo
                        data_finalizacao = data_inicial + timedelta(days = prazo)
                        
                        # Verifica se status é A fazer ou Fazendo e calcula data fim conforme início e prazo
                        if status == 'A fazer' or status == 'Fazendo':
                            data_fim = data_finalizacao

                        tarefa = Tarefa(
                            id_empresa=usuario.id_empresa, descri=descricaoTarefa, stat=status.capitalize(), prioridade=prioridade, data_ini=data_inicial, data_real=data_real, data_finalizacao=data_finalizacao, 
                            data_fim=data_fim, prazo=prazo, id_tamanho=id_tamanho, porcentagem=porcentagem, id_departamento=id_departamento, id_centro_custo=id_centro_custo, autoridade=autoridade,
                            responsavel=responsavel, historico=historicoTarefa, status_pendencia=status_pendencia,processo_relacionado=processo_relacionado,
                            pendente_por=pendente_por, checado=checado, id_pessoa=id_pessoa, id_update=id_pessoa, last_update=datetime.now()
                        )
                        tarefa.save()
                        
                        #Se o campo executor estiver vazio irá inserir no banco o valor nulo
                        executor1 = Pessoa.objects.get(nome=executor1)

                        if executor2 == '':
                            executor2 = None
                        else:
                            executor2 = Pessoa.objects.get(nome=executor2)
                        if executor3 == '':
                            executor3 = None
                        else:
                            executor3 = Pessoa.objects.get(nome=executor3)
                        if executor4 == '':
                            executor4 = None
                        else:
                            executor4 = Pessoa.objects.get(nome=executor4)
                        if executor5 == '':
                            executor5 = None
                        else:
                            executor5 = Pessoa.objects.get(nome=executor5)
                        if executor6 == '':
                            executor6 = None
                        else:
                            executor6 = Pessoa.objects.get(nome=executor6)
                        if executor7 == '':
                            executor7 = None
                        else:
                            executor7 = Pessoa.objects.get(nome=executor7)
                        if executor8 == '':
                            executor8 = None
                        else:
                            executor8 = Pessoa.objects.get(nome=executor8)
                        if executor9 == '':
                            executor9 = None
                        else:
                            executor9 = Pessoa.objects.get(nome=executor9)
                        if executor10 == '':
                            executor10 = None
                        else:
                            executor10 = Pessoa.objects.get(nome=executor10)

                        #Se o valor de porcentagem por executor não existir ele irá inserir no banco o valor nulo
                        if porcento2 == '':
                            porcento2 = None
                        if porcento3 == '':
                            porcento3 = None
                        if porcento4 == '':
                            porcento4 = None
                        if porcento5 == '':
                            porcento5 = None
                        if porcento6 == '':
                            porcento6 = None
                        if porcento7 == '':
                            porcento7 = None
                        if porcento8 == '':
                            porcento8 = None
                        if porcento9 == '':
                            porcento9 = None
                        if porcento10 == '':
                            porcento10 = None

                        executor = Executor(
                            id_tarefa=get_object_or_404(Tarefa, id_tarefa=tarefa.id_tarefa), executor1=executor1, executor2=executor2, executor3=executor3,
                            executor4=executor4,executor5=executor5,executor6=executor6,executor7=executor7,executor8=executor8,
                            executor9=executor9,executor10=executor10, porcento1=porcento1, porcento2=porcento2, porcento3=porcento3,
                            porcento4=porcento4,porcento5=porcento5,porcento6=porcento6,porcento7=porcento7,porcento8=porcento8,
                            porcento9=porcento9,porcento10=porcento10
                        )
                            
                        executor.save()

                        try:
                            solicitacao1 = Solicitacao(
                                empreendimento=empreendimento, bloco=bloco, unidade=apto, proprietario_nome=proprietario_nome,
                                proprietario_email=proprietario_email, solicitante_nome=solicitante_nome, solicitante_email=solicitante_email,
                                telefone1=telefone1, telefone2=telefone2, status_processo=status_processo, status_solicitacao=status_solicitacao,
                                tipo_solicitacao=tipo_solicitacao, data_entrega=data_entrega, satisfacao_avaliacao=int(satisfacao_avaliacao), 
                                satisfacao_observacoes=satisfacao_observacoes, id_tarefa=get_object_or_404(Tarefa, id_tarefa=tarefa.id_tarefa)
                            )
                            solicitacao1.save()
                        except:
                            solicitacao1 = Solicitacao(
                                empreendimento=empreendimento, bloco=bloco, unidade=apto, proprietario_nome=proprietario_nome,
                                proprietario_email=proprietario_email, solicitante_nome=solicitante_nome, solicitante_email=solicitante_email,
                                telefone1=telefone1, status_processo=status_processo, id_tarefa=get_object_or_404(Tarefa, id_tarefa=tarefa.id_tarefa)
                            )
                            solicitacao1.save()

                        try:
                            i = 0
                            for ambi in ambiente:
                                if ambi != '':
                                    if finalizado[i] == "Sim":
                                        finalizado[i] = 1
                                    else:
                                        finalizado[i] = 0
                                    problema = Problema(
                                        finalizado = finalizado[i], ambiente = ambiente[i], descricao_sat = descricao[i], tipo_reparo = tipo_reparo[i],
                                        procedencia = procedencia[i], historico_sat = historico[i], estimativa_custo = estimativa_custo[i], duracao = duracao[i],
                                        material = material[i], id_solicitacao=get_object_or_404(Solicitacao, id_solicitacao=solicitacao1.id_solicitacao)
                                    )
                                    problema.save()
                                    i += 1
                        except:
                            problema = Problema(id_solicitacao=get_object_or_404(Solicitacao, id_solicitacao=solicitacao1.id_solicitacao))

                        # id/linha: 0, descrição: 1, porcentagem: 6, prioridade: 2, c.c: 3, departamento: 35, status: 4, result
                        solicitacao = Solicitacao(  id_solicitacao = linha, status_solicitacao = dados.row(linha)[1].value,  proprietario_nome = int(dados.row(linha)[6].value),
                                                    proprietario_email = int(dados.row(linha)[2].value), solicitante_nome = dados.row(linha)[3].value, solicitante_email = dados.row(linha)[35].value,
                                                    telefone1 = dados.row(linha)[4].value                
                        )
                        solicitacao.save()
                        solicitacao.result = 'Cadastrada com sucesso'
                        solicitacoes.append(solicitacao)
                except:
                    solicitacao.result = 'Falha no cadastro'
                    solicitacoes.append(solicitacao)

        os.remove(uploaded_file_url)
    
    context = {
        "usuario": usuario,
        "solicitacoes" : solicitacoes,
    }
    

    return render(request, "importarSolicitacao.html", context)

def getExecutores(tarefa):
    Executores = tarefa.executor1

    if tarefa.executor2 != None:
        Executores = Executores + "," + tarefa.executor2

    if tarefa.executor3 != None:
        Executores = Executores + "," + tarefa.executor3

    if tarefa.executor4 != None:
        Executores = Executores + "," + tarefa.executor4

    if tarefa.executor5 != None:
        Executores = Executores + "," + tarefa.executor5

    if tarefa.executor6 != None:
        Executores = Executores + "," + tarefa.executor6

    if tarefa.executor7 != None:
        Executores = Executores + "," + tarefa.executor7

    if tarefa.executor8 != None:
        Executores = Executores + "," + tarefa.executor8

    if tarefa.executor9 != None:
        Executores = Executores + "," + tarefa.executor9

    if tarefa.executor10 != None:
        Executores = Executores + "," + tarefa.executor10
    
    return Executores