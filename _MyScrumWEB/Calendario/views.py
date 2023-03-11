from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Import de outros Apps
from _Login.models import Pessoa, Vinculos
from _Login.views import get_user
from Home.models import TarefasHome
from Departamento.models import Departamento
from Centro_de_custo.models import CentroCusto
from Feriado.models import Feriados
from Tarefa.models import Tarefa, Executor
from Tarefa.forms import TarefaForms
from Processo.models import Processos
from _MyScrumWEB import urls
from Etapa.models import Etapas
from Sub_etapa.models import SubEtapas
from Kanban.models import TarefasKanban

from .models import TarefasCalendario

# Import Biblioteca Python
from datetime import date, datetime, timedelta
from random import randint
import json
import threading
import time


# Create your views here.

@login_required(login_url=urls.getUrlSubdominio())
def calendario(request):
    descri_pesquisa = ""
    # usuarios = request.GET.getlist('pessoa')
    usuario = get_user(request.user)

    if len(request.GET.getlist('pessoa')) == 0 and request.GET.get('start') == None:
        pessoas = [get_user(request.user).nome]
    else:
        pessoas = request.GET.getlist('pessoa')


    # if len(usuarios) == 1:
    #     user = Pessoa.objects.get(nome=usuarios[0]).id_user
    #     usuario = get_user(user)
    #     usuarios.append('valor para não bugar a tupla')

    # if len(usuarios) == 0:
    #     user = request.user
    #     usuario = get_user(user)
    #     usuarios.append(usuario.nome)
    #     usuarios.append('valor para não bugar a tupla')

    tarefas = []
    filtros = {}
    filtrosCC = ""
    filtrosProcesso = ""
    filtrosDPTO = ""
    filtrosAutoridade = ""
    filtrosResponsavel = ""
    filtrosPessoa = ""
    filtrosExecutor = ""
    filtrosImpedimento = ""
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
    ################# Filtro de Processo ##########################
    processos = request.GET.getlist('processo')
    if len(processos):
        filtros['processo'] = processos
        processos = str(processos).replace('[','(').replace(']',')')
        filtrosProcesso = f''' processo_relacionado in {processos} AND '''
    ################# Filtro de Processo ##########################
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

    if len(request.GET.getlist('pessoa')) == 0 and request.GET.get('start') == None:
        pessoas = [get_user(request.user).nome]

    if len(pessoas) > 0:
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
    
    
    WHERE = f"""
    {filtrosCC}
    {filtrosProcesso}
    {filtrosDPTO}
    {filtrosAutoridade}
    {filtrosResponsavel}
    {filtrosPessoa}
    {filtrosExecutor}

    CASE 
        WHEN calendario = 1 and id_empresa = '{usuario.id_empresa}'
            THEN stat != 'Cancelado'
    END
    """
    
    centrocustos = CentroCusto.objects.all().exclude(id_sienge = None)
    aFazer = []
    Fazendo = []
    Feito = []
    tarefas = TarefasCalendario.objects.extra(where=[WHERE])
    departamentos = Departamento.objects.all()
    processos = Processos.objects.all()
    pessoas = Pessoa.objects.all()

    #################--------------------------------#########################
    ################# Verificando o status da tarefa #########################
    for tarefa in tarefas:
        if tarefa.stat == 'A fazer':
            tarefa.data_ini = tarefa.data_ini.strftime('%d/%m/%Y')
            tarefa.data_fim = tarefa.data_fim.strftime('%d/%m/%Y')
            aFazer.append(tarefa)
        elif tarefa.stat == 'Fazendo':
            tarefa.data_ini = tarefa.data_ini.strftime('%d/%m/%Y')
            tarefa.data_fim = tarefa.data_fim.strftime('%d/%m/%Y')
            Fazendo.append(tarefa)
        elif tarefa.stat == 'Feito':
            tarefa.data_ini = tarefa.data_ini.strftime('%d/%m/%Y')
            tarefa.data_fim = tarefa.data_fim.strftime('%d/%m/%Y')
            Feito.append(tarefa)
    ################# Verificando o status da tarefa #########################
    #################--------------------------------#########################
    
    context = {
        'aFazer' : aFazer,
        'Fazendo' : Fazendo,
        'Feito' : Feito,
        'centrocustos' : centrocustos,
        'filtros' : filtros,
        'usuario' : usuario,
        'departamentos' : departamentos,
        'processos' : processos,
        'pessoas' : pessoas,
        'tarefas' : list(tarefas.values())
    }

    return render(request, 'calendario.html', context)




