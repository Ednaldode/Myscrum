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
from Processo.models import Processos
from _MyScrumWEB import urls
from Etapa.models import Etapas
from Sub_etapa.models import SubEtapas
from Kanban.models import TarefasKanban

# Import Biblioteca Python
from datetime import date, datetime, timedelta
from random import randint
import json
import threading
import time


# Create your views here.

@login_required(login_url=urls.getUrlSubdominio())
def espelho(request):
    descri_pesquisa = ""
    usuarios = request.GET.getlist('pessoa')
    usuario = "Varios Usuarios"

    if len(usuarios) == 1:
        user = Pessoa.objects.get(nome=usuarios[0]).id_user
        usuario = get_user(user)
        usuarios.append('valor para não bugar a tupla')

    if len(usuarios) == 0:
        user = request.user
        usuario = get_user(user)
        usuarios.append(usuario.nome)
        usuarios.append('valor para não bugar a tupla')
        
    tarefas = []
    filtros = {}
    filtrosCC = ""


    #################--------------------##########################
    ################# Filtro de Centro de custo ##################
    # Se o campo centrocusto não estiver vazio filtra tarefas baseada no centrocusto de custo escolhido
    if request.GET.get('centrocusto') != None and request.GET.get('centrocusto') != 'Centros de custo':
        filtros['centrocusto'] = CentroCusto.objects.get(id_centro_custo=request.GET.get('centrocusto')).centrocusto
        centro_custo = CentroCusto.objects.get(id_centro_custo=request.GET.get('centrocusto')).centrocusto
        filtrosCC = f''' centro_custo = '{centro_custo}' AND '''
    ################# Filtro de Centro de custo ##################
    #################--------------------##########################
    
    WHERE = f"""
    {filtrosCC}

    """
    
    centrocustos = CentroCusto.objects.all().exclude(id_sienge = None)

    context = {
        'centrocustos' : centrocustos,
        'filtros' : filtros,
        'usuario' : usuario,
    }

    return render(request, 'espelhovendas.html', context)


def vistoria(request):
    descri_pesquisa = ""
    usuarios = request.GET.getlist('pessoa')
    usuario = "Varios Usuarios"

    if len(usuarios) == 1:
        user = Pessoa.objects.get(nome=usuarios[0]).id_user
        usuario = get_user(user)
        usuarios.append('valor para não bugar a tupla')

    if len(usuarios) == 0:
        user = request.user
        usuario = get_user(user)
        usuarios.append(usuario.nome)
        usuarios.append('valor para não bugar a tupla')
        
    tarefas = []
    filtros = {}
    filtrosCC = ""


    #################--------------------##########################
    ################# Filtro de Centro de custo ##################
    # Se o campo centrocusto não estiver vazio filtra tarefas baseada no centrocusto de custo escolhido
    if request.GET.get('centrocusto') != None and request.GET.get('centrocusto') != 'Centros de custo':
        filtros['centrocusto'] = CentroCusto.objects.get(id_centro_custo=request.GET.get('centrocusto')).centrocusto
        centro_custo = CentroCusto.objects.get(id_centro_custo=request.GET.get('centrocusto')).centrocusto
        filtrosCC = f''' centro_custo = '{centro_custo}' AND '''
    ################# Filtro de Centro de custo ##################
    #################--------------------##########################
    
    WHERE = f"""
    {filtrosCC}

    """
    centrocustos = CentroCusto.objects.all().exclude(id_sienge = None)
    context = {
        'centrocustos' : centrocustos,
        'filtros' : filtros,
        'usuario' : usuario,
    }

    return render(request, 'espelhovistorias.html', context)

def pendencias(request):
    descri_pesquisa = ""
    usuarios = request.GET.getlist('pessoa')
    usuario = "Varios Usuarios"

    if len(usuarios) == 1:
        user = Pessoa.objects.get(nome=usuarios[0]).id_user
        usuario = get_user(user)
        usuarios.append('valor para não bugar a tupla')

    if len(usuarios) == 0:
        user = request.user
        usuario = get_user(user)
        usuarios.append(usuario.nome)
        usuarios.append('valor para não bugar a tupla')
        
    tarefas = []
    filtros = {}
    filtrosCC = ""


    #################--------------------##########################
    ################# Filtro de Centro de custo ##################
    # Se o campo centrocusto não estiver vazio filtra tarefas baseada no centrocusto de custo escolhido
    if request.GET.get('centrocusto') != None and request.GET.get('centrocusto') != 'Centros de custo':
        filtros['centrocusto'] = CentroCusto.objects.get(id_centro_custo=request.GET.get('centrocusto')).centrocusto
        centro_custo = CentroCusto.objects.get(id_centro_custo=request.GET.get('centrocusto')).centrocusto
        filtrosCC = f''' centro_custo = '{centro_custo}' AND '''
    ################# Filtro de Centro de custo ##################
    #################--------------------##########################
    
    WHERE = f"""
    {filtrosCC}

    """
    centrocustos = CentroCusto.objects.all().exclude(id_sienge = None)
    context = {
        'centrocustos' : centrocustos,
        'filtros' : filtros,
        'usuario' : usuario,
    }

    return render(request, 'pendenciasvistoria.html', context)

    


