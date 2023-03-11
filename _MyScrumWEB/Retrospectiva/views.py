# Import Django
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.serializers import serialize
from django.http.response import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.template.loader import render_to_string

# Import de outros Apps
from _Login.models import Pessoa, Vinculos
from Departamento.models import Departamento
from Centro_de_custo.models import CentroCusto
from Tarefa.models import Tarefa, Executor, Retrospectiva
from Tarefa.forms import TarefaForms
from _Login.views import get_user
from Processo.models import Processos
from _MyScrumWEB import urls
from Kanban.views import editarTarefa, exibirTarefa, getExecutores

# Import de mesmo App
from .models import TarefasRetrospectiva, ExportarRetrospectiva

# Import Biblioteca Python
from datetime import date, datetime, timedelta
import json
import xlrd
import xlwt
import os

# Create your views here.
# Função que gera os filtros baseado no form do request 
def gerarFiltros(request, usuario):
    filtros = {}
    filtrosHierarquia = ""
    filtrosStatus = ""
    filtrosCC = ""
    filtrosBlocos = ""
    filtrosUnidades = ""
    filtrosProcesso = ""
    filtrosPessoa = ""
    filtrosExecutor = ""
    filtrosImpedimento = ""
    filtrosProprietario = ""
    filtrosContatos = ""
    filtrosEmails = ""
    filtrosReparo = ""
    
    filtrosEscritorio = ""
    filtrosPChave = ""
    filtrosNProcesso = ""
    filtrosAutor = ""
    filtrosReu = ""
    filtrosTestemunha = ""
    filtrosPreposto = ""

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
            data_inicio = date(hoje.year, hoje.month, 1 )
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
    #################------------------############################

    #################---------------------------##################
    ################# Filtro de Centro de custo ##################
    # Se o campo centrocusto não estiver vazio filtra tarefas baseada no centrocusto de custo escolhido
    if request.GET.get('centrocusto') != None and request.GET.get('centrocusto') != 'Centros de custo':
        filtros['centrocusto'] = CentroCusto.objects.get(id_centro_custo=request.GET.get('centrocusto')).centrocusto
        centro_custo = CentroCusto.objects.get(id_centro_custo=request.GET.get('centrocusto')).centrocusto
        filtrosCC = f''' centro_custo = '{centro_custo}' AND '''
    ################# Filtro de Centro de custo ##################
    #################---------------------------##################

    #################-------------------##########################
    ################# Filtro de Bloco ############################
    blocos = request.GET.getlist('bloco')
    if len(blocos):
        filtros['bloco'] = blocos
        blocos = str(blocos).replace('[','(').replace(']',')')
        filtrosBlocos = f''' bloco in {blocos} AND '''
    ################# Filtro de Bloco ############################
    #################-------------------##########################

    #################-------------------############################
    ################# Filtro de Unidade ############################
    unidades = request.GET.getlist('unidade')
    if len(unidades):
        filtros['unidade'] = unidades
        unidades = str(unidades).replace('[','(').replace(']',')')
        filtrosUnidades = f''' unidade in {unidades} AND '''
    print(filtrosUnidades)
    ################# Filtro de Unidade ##########################
    #################-------------------##########################

    #################---------------------------############################
    ################# Filtro de Status Processo ############################
    processos = request.GET.getlist('processo')
    if len(processos):
        filtros['processo'] = processos
        processos = str(processos).replace('[','(').replace(']',')')
        filtrosProcesso = f''' status_processo in {processos} AND '''
    ################# Filtro de Status Processo ############################
    #################---------------------------############################

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

    #################------------------------########################
    ################# Filtro de Proprietário ########################
    proprietarios = request.GET.getlist('proprietario')
    if len(proprietarios):
        filtros['proprietario'] = proprietarios
        proprietarios = str(proprietarios).replace('[','(').replace(']',')')
        filtrosProprietario = f''' proprietario_nome in {proprietarios} AND'''
    ################# Filtro de Proprietário ########################
    #################------------------------########################
    
    #################-------------------########################
    ################# Filtro de Contato ########################
    contatos = request.GET.getlist('contato')
    if len(contatos):
        filtros['contato'] = contatos
        contatos = str(contatos).replace('[','(').replace(']',')')
        filtrosContatos = f''' telefone1 in {contatos} AND'''
    ################# Filtro de Contato ########################
    #################-------------------########################

    #################-----------------########################
    ################# Filtro de Email ########################
    emails = request.GET.getlist('email')
    if len(emails):
        filtros['email'] = emails
        emails = str(emails).replace('[','(').replace(']',')')
        filtrosEmails = f''' proprietario_email in {emails} AND'''
    ################# Filtro de Email ########################
    #################-----------------########################

    #################------------------############################
    ################# Filtro de Reparo ############################
    reparos = request.GET.getlist('reparo')
    if len(reparos):
        filtros['reparo'] = reparos
        reparos = str(reparos).replace('[','(').replace(']',')')
        filtrosReparo = f''' tipo_reparo in {reparos} AND'''
    ################# Filtro de Reparo ############################
    #################--------------------##########################

    #################--------------------############################
    ################# Filtro de Impedimento #########################
    impedimentos = request.GET.getlist('impedimento')
    if len(impedimentos):
        filtros['impedimento'] = impedimentos
        impedimentos = str(impedimentos).replace('[','(').replace(']',')')
        filtrosImpedimento = f''' pendente_por in {impedimentos} AND '''
    ################# Filtro de Impedimento #########################
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

    #################---------------------------############################
    #################   Filtro de Escritório    ############################
    escritorios = request.GET.getlist('escritorio')
    if len(escritorios):
        filtros['escritorio'] = escritorios
        escritorios = str(escritorios).replace('[','(').replace(']',')')
        filtrosEscritorio = f''' escritorio in {escritorios} AND '''
    #################   Filtro de Escritório    ############################
    #################---------------------------############################

    #################---------------------------############################
    #################    Filtro de Processo     ############################
    processos = request.GET.getlist('numero_processo')
    if len(processos):
        filtros['numero_processo'] = processos
        processos = str(processos).replace('[','(').replace(']',')')
        filtrosProcesso = f''' numero_processo in {processos} AND '''
    #################    Filtro de Processo     ############################
    #################---------------------------############################

    #################---------------------------############################
    #################    Filtro de Processo     ############################
    palavra_chave = request.GET.getlist('palavra_chave')
    if len(palavra_chave):
        filtros['palavra_chave'] = palavra_chave
        palavra_chave = str(palavra_chave).replace('[','(').replace(']',')')
        filtrosProcesso = f''' (numero_processo in {palavra_chave} OR
        autor2 in {palavra_chave} OR
        autor3 in {palavra_chave} OR
        autor4 in {palavra_chave} OR
        autor5 in {palavra_chave} OR
        autor6 in {palavra_chave} OR
        autor7 in {palavra_chave} OR
        autor8 in {palavra_chave} OR
        autor9 in {palavra_chave} OR
        autor10 in {palavra_chave}) AND '''
    #################    Filtro de Processo     ############################
    #################---------------------------############################

    #################--------------------############################
    #################   Filtro de Autor  ############################
    autores = request.GET.getlist('autor')
    if len(autores):
        filtros['autor'] = autores
        autores = str(autores).replace('[','(').replace(']',')')
        filtrosAutor = f''' (autor1 in {autores} OR
        autor2 in {autores} OR
        autor3 in {autores} OR
        autor4 in {autores} OR
        autor5 in {autores} OR
        autor6 in {autores} OR
        autor7 in {autores} OR
        autor8 in {autores} OR
        autor9 in {autores} OR
        autor10 in {autores}) AND'''
    #################   Filtro de Autor  ############################
    #################--------------------############################

    #################--------------------############################
    #################   Filtro de Reu    ############################
    reus = request.GET.getlist('reu')
    if len(reus):
        filtros['reu'] = reus
        reus = str(reus).replace('[','(').replace(']',')')
        filtrosReu = f''' (reu1 in {reus} OR
        reu2 in {reus} OR
        reu3 in {reus} OR
        reu4 in {reus} OR
        reu5 in {reus} OR
        reu6 in {reus} OR
        reu7 in {reus} OR
        reu8 in {reus} OR
        reu9 in {reus} OR
        reu10 in {reus}) AND'''
    #################   Filtro de Reu    ############################
    #################--------------------############################

    #################------------------------########################
    #################  Filtro de Testemunha  ########################
    testemunhas = request.GET.getlist('testemunha')
    if len(testemunhas):
        filtros['testemunha'] = testemunhas
        testemunhas = str(testemunhas).replace('[','(').replace(']',')')
        filtrosTestemunha = f''' (testemunha1 in {testemunhas} OR
        testemunha2 in {testemunhas} OR
        testemunha3 in {testemunhas} OR
        testemunha4 in {testemunhas} OR
        testemunha5 in {testemunhas} OR
        testemunha6 in {testemunhas} OR
        testemunha7 in {testemunhas} OR
        testemunha8 in {testemunhas} OR
        testemunha9 in {testemunhas} OR
        testemunha10 in {testemunhas}) AND'''
    #################------------------------########################
    #################  Filtro de Testemunha  ########################

    WHERE = f"""
    {filtrosHierarquia}
    {filtrosStatus}
    {filtrosProcesso}
    {filtrosCC}
    {filtrosBlocos}
    {filtrosUnidades}
    {filtrosPessoa}
    {filtrosExecutor}
    {filtrosImpedimento}
    {filtrosProprietario}
    {filtrosContatos}
    {filtrosEmails}
    {filtrosReparo}
    {filtrosEscritorio}
    {filtrosNProcesso}
    {filtrosAutor}
    {filtrosReu}
    {filtrosTestemunha}

    {filtrosPChave}
    {filtrosPreposto}

    CASE 
        WHEN stat = 'A fazer' and id_empresa = {usuario.id_empresa}
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim < '{data_inicio}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}'
        WHEN stat = 'Fazendo' and id_empresa = {usuario.id_empresa}
            THEN 
                stat != 'Cancelado'
        WHEN stat = 'Feito' and id_empresa = {usuario.id_empresa} or stat = 'Cancelado' and id_empresa = {usuario.id_empresa}
            THEN
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}'
    END
    """

    retorno = {
        'filtros' : filtros,
        'WHERE' : WHERE,
        'status' : status
    }

    return retorno


def exportarRetrospectivas(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    data = datetime.now().strftime('%Y-%m-%d')

    model = 'ExportarRetrospectiva'

    filename = f'MyScrum Solicitações - Conservação / Limpeza {data} ({usuario.nome}).xls'
    
    queryset = ExportarRetrospectiva.objects.all().extra(where=[filtrosWhere['WHERE']]).values_list(
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
        'r5w2hT',
        'retrospec',
        'descricao',
        'stats',
        'id_responsavel',
        'finalizado',
        'r_historico',
        'nome_responsavel',
        
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
        'r5w2hT',
        'retrospec',
        'descricao',
        'stats',
        'id_responsavel',
        'finalizado',
        'r_historico',
        'nome_responsavel',
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

def retrospectiva(request):
    usuario = get_user(request.user)

    retrospectivas = []
    filtros = {}
    filtrosHierarquia = ""
    filtrosStatus = ""
    filtrosCC = ""
    filtrosDPTO = ""
    filtrosProcesso = ""
    filtrosAutoridade = ""
    filtrosResponsavel = ""
    filtrosPessoa = ""
    filtrosExecutor = ""
    filtros5w2h = ""
    form = TarefaForms(request)

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
            data_inicio = date(hoje.year, hoje.month, 1 )
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
    
    filtros['status'] = status
    
    if len(status) != 0:
        status = str(status).replace('[','(').replace(']',')')
    else:
        status = "('A fazer', 'Fazendo', 'Feito')"

    filtrosStatus = f''' stats in {status} AND '''
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
        departamento in {vinculosDPTO} OR
        centro_custo in {vinculosCC} OR
        '{usuario.nome}' in (executor1, executor2, executor3, executor4, executor5, executor6, executor7, executor8, executor9, executor10)) AND '''
    ################# Filtro de Hierarquia ##########################
    #################--------------------############################

    # is_staff = 0, Usuario = tem acesso apenas as tarefas onde contem o seu nome
    # is_staff = 1, Administrador = tem acesso a todas Tarefas
    # is_staff = 2, Lider = tem acessso as tarefas com seu nome e as tarefas do seu departamento
    # is_staff = 3, Gestor = tem acesso as tarefas com sue nome e as tarefas do seu centro custo

    WHERE = f"""
    {filtrosHierarquia}
    {filtrosStatus}
    {filtrosCC}
    {filtrosDPTO}
    {filtrosProcesso}
    {filtrosAutoridade}
    {filtrosResponsavel}
    {filtrosPessoa}
    {filtrosExecutor}

    CASE 
        WHEN retrospec = 'Foi bom' or retrospec = 'Pode melhorar' or retrospec = 'Deve melhorar'
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
    END
    """
    retrospectivas = TarefasRetrospectiva.objects.extra(where=[WHERE]).order_by('prioridade')


    foiBom = []
    podeMelhorar = []
    deveMelhorar = []
    pessoas = Pessoa.objects.all()
    departamentos = Departamento.objects.all()
    centrocustos = CentroCusto.objects.all()
    processos = Processos.objects.all()

    for retrospectiva in retrospectivas:
        if retrospectiva.retrospec == 'Foi bom':
            retrospectiva.Executores = getExecutores(retrospectiva)
            retrospectiva.data_ini = retrospectiva.data_ini.strftime('%d/%m/%Y')
            retrospectiva.data_fim = retrospectiva.data_fim.strftime('%d/%m/%Y')
            retrospectiva.data_finalizacao = retrospectiva.data_finalizacao.strftime('%d/%m/%Y')
            foiBom.append(retrospectiva)
        elif retrospectiva.retrospec == 'Pode melhorar':
            retrospectiva.Executores = getExecutores(retrospectiva)
            retrospectiva.data_ini = retrospectiva.data_ini.strftime('%d/%m/%Y')
            retrospectiva.data_fim = retrospectiva.data_fim.strftime('%d/%m/%Y')
            retrospectiva.data_finalizacao = retrospectiva.data_finalizacao.strftime('%d/%m/%Y')
            podeMelhorar.append(retrospectiva)
        elif retrospectiva.retrospec == 'Deve melhorar':
            retrospectiva.Executores = getExecutores(retrospectiva)
            retrospectiva.data_ini = retrospectiva.data_ini.strftime('%d/%m/%Y')
            retrospectiva.data_fim = retrospectiva.data_fim.strftime('%d/%m/%Y')
            retrospectiva.data_finalizacao = retrospectiva.data_finalizacao.strftime('%d/%m/%Y')
            deveMelhorar.append(retrospectiva)
    
    context = {
        'foiBom' : foiBom,
        'podeMelhorar' : podeMelhorar,
        'deveMelhorar' : deveMelhorar,
        'pessoas' : pessoas,
        'departamentos' : departamentos,
        'centrocustos' : centrocustos,
        'processos' : processos,
        'filtros' : filtros,
        'usuario' : usuario,
        'form' : form,
        'status' : status      
    }

    return render(request, 'retrospectiva.html', context)
