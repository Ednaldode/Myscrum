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

# Import do mesmo app
from .objetosGrafico import GraficoDemanda, GraficoProcedimento, GraficoCC

# Create your views here.

@login_required(login_url=urls.getUrlSubdominio())
def analisarDash(request):
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
    filtrosHierarquia = ""
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

    #################--------------------##########################
    ################# Filtro de Datas #############################
    # Se existir valor na data usamos o valor escolhido, se não usamos o valor do periodo atual
    if request.GET.get('start') != None and request.GET.get('end') != None :
        data_inicio = datetime.strptime(request.GET.get('start'), '%d/%m/%Y').date()
        data_fim = datetime.strptime(request.GET.get('end'), '%d/%m/%Y').date()
        
        filtros['start'] = data_inicio.strftime("%d/%m/%Y")
        filtros['end'] = data_fim.strftime("%d/%m/%Y")

        descri_pesquisa = f'''Periodo do dia {filtros['start']} até {filtros['end']}'''

    else:
        hoje = date.today()

        data_inicio = hoje
        data_fim = hoje + timedelta(weeks=1)

        filtros['start'] = data_inicio.strftime("%d/%m/%Y")
        filtros['end'] = data_fim.strftime("%d/%m/%Y")

        descri_pesquisa = f'''Periodo do dia {filtros['start']} até {filtros['end']}'''

    ################# Filtro de Datas #############################
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
    # Se o campo processo não estiver vazio filtra tarefas baseada na SubEtapa escolhido
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

    WHERE = f"""
    {filtrosHierarquia}
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

    CASE 
        WHEN stat = 'A fazer'
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim < '{data_inicio}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Feito'
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Fazendo'
            THEN stat != 'Cancelado'
    END
    """
    tarefas = TarefasHome.objects.extra(where=[WHERE])
    
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

    impedimentos = tarefas.filter(pendente_por__in=usuarios)
    impedimentos = len(impedimentos)

    WHERE = f"""
    responsavel in {tuple(usuarios)} OR
    autoridade in {tuple(usuarios)} OR
    checado in {tuple(usuarios)} OR
    pendente_por in {tuple(usuarios)} OR
    executor1 in {tuple(usuarios)} OR
    executor2 in {tuple(usuarios)} OR
    executor3 in {tuple(usuarios)} OR
    executor4 in {tuple(usuarios)} OR
    executor5 in {tuple(usuarios)} OR
    executor6 in {tuple(usuarios)} OR
    executor7 in {tuple(usuarios)} OR
    executor8 in {tuple(usuarios)} OR
    executor9 in {tuple(usuarios)} OR
    executor10 in {tuple(usuarios)}
    """
    tarefas_filtradas = tarefas.extra(where=[WHERE])

    afazer = len(tarefas_filtradas.filter(stat='A fazer'))
    fazendo = len(tarefas_filtradas.filter(stat='Fazendo'))
    feito = len(tarefas_filtradas.filter(stat='Feito'))

    graficoVelocimetro = {
        'pontos' : 0
    }

    graficoProdutividade = {
        'previsto' : 0,
        'periodo' : 0,
        'realizado' : 0
    }

    dadosGraficoDemanda = []
    graficoDemanda = {
        'processos' : [],
        'pontos' : [],
        'cores' : []
    }

    dadosGraficoProcedimento = []
    graficoPrevistoXRealizado = {
        'processos' : [],
        'realizado' : [],
        'atrasado' : [],
        'impedimento' : []
    }

    dadosGraficoCC = []
    graficoCC = []


    # Percorrendo as tarefas e fazendo os calculos
    for tarefa in tarefas_filtradas:
        velocimetro = threading.Thread(target=CalcularVelocimetro, args=(graficoVelocimetro, tarefa, data_inicio, data_fim, usuarios))
        velocimetro.start()
        #CalcularVelocimetro(valores=graficoVelocimetro, tarefa=tarefa, data_inicio=data_inicio, data_fim=data_fim, usuarios=usuarios)
        
        produtividade = threading.Thread(target=CalcularProdutividade, args=(graficoProdutividade, tarefa, data_inicio, data_fim, usuarios))
        produtividade.start()
        #retorno = CalcularProdutividade(valores=graficoProdutividade, tarefa=tarefa, data_inicio=data_inicio, data_fim=data_fim, usuarios=usuarios)
        #graficoProdutividade['previsto'] += retorno['previsto']
        #graficoProdutividade['periodo'] += retorno['periodo']
        #graficoProdutividade['realizado'] += retorno['realizado']

        # START GraficoDemanda
        retorno = CalcularDemanda(tarefa=tarefa, data_inicio=data_inicio, data_fim=data_fim, usuarios=usuarios)
        for dados in dadosGraficoDemanda:
            if dados.get_processo() == retorno['processo']:
                dados.addPontos(retorno['pontos'])
                retorno = None
                break
        if retorno != None:
            dadosGraficoDemanda.append(GraficoDemanda(retorno['processo'], retorno['pontos'], gerarCor()))
        # END GraficoDemanda
        
        # START GraficoProcedimento
        retorno = CalcularPrevistoXRealizado(tarefa=tarefa, data_inicio=data_inicio, data_fim=data_fim, usuarios=usuarios)
        for dados in dadosGraficoProcedimento:
            if dados.get_processo() == retorno['processo']:
                dados.addRealizado(retorno['realizado'])
                dados.addAtrasado(retorno['atraso'])
                dados.addImpedimento(retorno['impedimento'])
                retorno = None
                break
            
        if retorno != None:
            dadosGraficoProcedimento.append(GraficoProcedimento(retorno['processo'], retorno['realizado'], retorno['atraso'], retorno['impedimento']))
        # END GraficoProcedimento

        # START GraficoCC
        retorno = CalcularCC(tarefa=tarefa, data_inicio=data_inicio, data_fim=data_fim, usuarios=usuarios)
        for dados in dadosGraficoCC:
            if dados.get_cc() == retorno['cc']:
                dados.addPontos(retorno['pontos'])
                retorno = None
                break

        if retorno != None:
            dadosGraficoCC.append(GraficoCC(retorno['cc'], retorno['pontos']))
        # END Grafico CC

    # Arredondando os valores e montando as listas

    # START Velocimetro 
    graficoVelocimetro['pontos'] = round(graficoVelocimetro['pontos'] / diasPercorridosPeriodo(data_inicio, data_fim), 2)
    # END Velocimetro

    # START Produtividade
    graficoProdutividade['previsto'] = int(graficoProdutividade['previsto'])
    graficoProdutividade['realizado'] = int(graficoProdutividade['realizado'])

    for user in usuarios:
        if user != 'valor para não bugar a tupla':
            graficoProdutividade['periodo'] += diasPercorridosPeriodo(data_inicio=data_inicio, data_fim=data_fim) * Pessoa.objects.get(nome=user).carga_horaria
    # END Produtividade

    # START GraficoDemanda
    dados_ordenados = sorted(dadosGraficoDemanda, key=GraficoDemanda.get_pontos, reverse=True)
    for dados in dados_ordenados:
        graficoDemanda['processos'].append(dados.get_processo())
        graficoDemanda['pontos'].append(dados.get_pontos())
        graficoDemanda['cores'].append(dados.get_cor())
    # END GraficoDemanda

    # START GraficoProcedimento
    dados_ordenados = sorted(dadosGraficoProcedimento, key=GraficoProcedimento.get_pontos, reverse=True)
    for dados in dados_ordenados:
        graficoPrevistoXRealizado['processos'].append(dados.get_processo())
        graficoPrevistoXRealizado['realizado'].append(dados.get_realizado())
        graficoPrevistoXRealizado['atrasado'].append(dados.get_atrasado())
        graficoPrevistoXRealizado['impedimento'].append(dados.get_impedimento())
    # END GraficoProcedimento

    # START GraficoCC
    dados_ordenados = sorted(dadosGraficoCC, key=GraficoCC.get_pontos, reverse=True)
    for dados in dados_ordenados:
        dic = {
            'nome' : dados.get_cc(),
            'pontos' : dados.get_pontos()
        }
        graficoCC.append(dic)

    if len(graficoCC) < 4:
        dic = {
            'nome' : 'Sem dados',
            'pontos' : 0
        }

        graficoCC.append(dic)
        graficoCC.append(dic)
        graficoCC.append(dic)
        graficoCC.append(dic)
        graficoCC.append(dic)
    # END GraficoCC

    context = {
        'afazer' : afazer,
        'fazendo' : fazendo,
        'feito' : feito,
        'impedimentos' : impedimentos,
        'pessoas' : pessoas,
        'departamentos' : departamentos,
        'centrocustos' : centrocustos,
        'etapas' : etapas,
        'subetapas' : subetapas,
        'processos' : processos,
        'filtros' : filtros,
        'usuario' : usuario,
        'graficoVelocimetro' : graficoVelocimetro,
        'graficoProdutividade' : graficoProdutividade,
        'graficoDemanda' : graficoDemanda,
        'graficoPrevistoXRealizado' : graficoPrevistoXRealizado,
        'descri_pesquisa' : descri_pesquisa,
        'graficoCC' :  graficoCC

    }

    return render(request, 'dashboard/dash.html', context)


def getFeriados():
    lista_feriados = []

    feriados = Feriados.objects.all()
    for feriado in feriados:
        lista_feriados.append(feriado.data_feriado)

    return lista_feriados

def diasNoPeriodo(data_inicio, data_fim, tarefa):
    dias_no_periodo = 0
    feriados = getFeriados()

    while data_inicio <= data_fim:
        if data_inicio >= tarefa.data_ini and data_inicio <= tarefa.data_fim and data_inicio not in feriados:
            dias_no_periodo += 1

        data_inicio = data_inicio + timedelta(days=1)
    
    return dias_no_periodo

def pesoDoDia(tarefa):
    dias_de_execucao = 0
    inicio = tarefa.data_ini
    fim = tarefa.data_fim
    feriados = getFeriados()

    while inicio <= fim:
        if inicio not in feriados:
            dias_de_execucao += 1 
        inicio = inicio + timedelta(days=1)
    

    return tarefa.tamanho / dias_de_execucao

def verificarAtuacao(tarefa, user, peso_da_tarefa):
    pontos = 0

    if tarefa.autoridade == user:
        pontos += peso_da_tarefa * 0.05

    if tarefa.responsavel == user:
        pontos += peso_da_tarefa * 0.15
    
    if tarefa.executor1 == user:
        pontos += (peso_da_tarefa * 0.8) * (tarefa.porcento1 / 100)
    
    if tarefa.executor2 == user:
        pontos += (peso_da_tarefa * 0.8) * (tarefa.porcento2 / 100)

    if tarefa.executor3 == user:
        pontos += (peso_da_tarefa * 0.8) * (tarefa.porcento3 / 100)

    if tarefa.executor4 == user:
        pontos += (peso_da_tarefa * 0.8) * (tarefa.porcento4 / 100)

    if tarefa.executor5 == user:
        pontos += (peso_da_tarefa * 0.8) * (tarefa.porcento5 / 100)

    if tarefa.executor6 == user:
        pontos += (peso_da_tarefa * 0.8) * (tarefa.porcento6 / 100)

    if tarefa.executor7 == user:
        pontos += (peso_da_tarefa * 0.8) * (tarefa.porcento7 / 100)

    if tarefa.executor8 == user:
        pontos += (peso_da_tarefa * 0.8) * (tarefa.porcento8 / 100)

    if tarefa.executor9 == user:
        pontos += (peso_da_tarefa * 0.8) * (tarefa.porcento9 / 100)

    if tarefa.executor10 == user:
        pontos += (peso_da_tarefa * 0.8) * (tarefa.porcento10 / 100)
    return pontos

def diasUteisPeriodo(data_inicio, data_fim):
    dias_uteis_periodo = 0
    feriados = getFeriados()

    while data_inicio <= data_fim:
        if data_inicio not in feriados:
            dias_uteis_periodo += 1
        data_inicio = data_inicio + timedelta(days=1)
    
    return dias_uteis_periodo

def diasPercorridosPeriodo(data_inicio, data_fim):
    dias_percorridos_periodo = 0
    feriados = getFeriados()

    if data_fim > date.today():
        data_fim = date.today()

    while data_inicio <= data_fim:
        if data_inicio not in feriados:
            dias_percorridos_periodo += 1
        data_inicio = data_inicio + timedelta(days=1)
    
    return dias_percorridos_periodo

def CalcularVelocimetro(valores, tarefa, data_inicio, data_fim, usuarios):
    if tarefa.stat == 'A fazer':
        valores['pontos'] += 0
        return 'Finalizado'

    if tarefa.stat == 'Feito':
        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            valores['pontos'] += 0
            return 'Finalizado'
        else:
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa = dias_no_periodo * peso_do_dia
            
            pontos_finais = 0
            for user in usuarios:
                pontos_finais += verificarAtuacao(tarefa, user, peso_da_tarefa)
            
            valores['pontos'] += pontos_finais
            return 'Finalizado'
    
    if tarefa.stat == 'Fazendo':
        if date.today() < data_fim:
            tarefa.data_fim = date.today()
        else:
            tarefa.data_fim = data_fim

        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            valores['pontos'] += 0
            return 'Finalizado'
        else: 
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa = (dias_no_periodo * peso_do_dia) * (tarefa.porcentagem / 100)

            pontos_finais = 0
            for user in usuarios:
                pontos_finais += verificarAtuacao(tarefa, user, peso_da_tarefa)

            valores['pontos'] += pontos_finais
            return 'Finalizado'

def CalcularProdutividade(valores, tarefa, data_inicio, data_fim, usuarios):
    #retorno = {
    #    'previsto' : 0,
    #    'periodo' : 0,
    #    'realizado' : 0
    #}

    if tarefa.stat == 'A fazer':
        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            return 'Finalizado'
        else:
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa = dias_no_periodo * peso_do_dia

            pontos_finais = 0
            for user in usuarios:
                pontos_finais += verificarAtuacao(tarefa, user, peso_da_tarefa)
            
            valores['previsto'] += pontos_finais

            return 'Finalizado'

    if tarefa.stat == 'Fazendo':
        if date.today() < data_fim:
            tarefa.data_fim = date.today()
        else:
            tarefa.data_fim = data_fim

        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            return 'Finalizado'
        else: 
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa_realizado = (dias_no_periodo * peso_do_dia) * (tarefa.porcentagem / 100)

            porcentagem_restante_tarefa = (100 - tarefa.porcentagem) / 100
            peso_da_tarefa_Arealizar = (dias_no_periodo * peso_do_dia) * porcentagem_restante_tarefa

            pontos_finais_realizado = 0
            pontos_finais_Arealizar = 0
            for user in usuarios:
                pontos_finais_realizado += verificarAtuacao(tarefa, user, peso_da_tarefa_realizado)
                pontos_finais_Arealizar += verificarAtuacao(tarefa, user, peso_da_tarefa_Arealizar)

            valores['realizado'] += pontos_finais_realizado
            valores['previsto'] += pontos_finais_Arealizar

            return 'Finalizado'

    if tarefa.stat == 'Feito':
        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            return 'Finalizado'
        else:
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa = dias_no_periodo * peso_do_dia

            pontos_finais = 0
            for user in usuarios:
                pontos_finais += verificarAtuacao(tarefa, user, peso_da_tarefa)
            
            valores['realizado'] += pontos_finais

            return 'Finalizado'
        
def CalcularDemanda(tarefa, data_inicio, data_fim, usuarios):
    retorno = {
        'processo' : tarefa.processo_relacionado,
        'pontos' : 0
    }

    if tarefa.stat == 'A fazer':
        retorno['pontos'] = 0
        return retorno

    if tarefa.stat == 'Feito':
        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            retorno['pontos'] = 0
            return retorno
        else:
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa = dias_no_periodo * peso_do_dia

            pontos_finais = 0
            for user in usuarios:
                pontos_finais += verificarAtuacao(tarefa, user, peso_da_tarefa)
            
            retorno['pontos'] = pontos_finais
            return retorno
    
    if tarefa.stat == 'Fazendo':
        if date.today() < data_fim:
            tarefa.data_fim = date.today()
        else:
            tarefa.data_fim = data_fim

        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            retorno['pontos'] = 0
            return retorno
        else: 
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa = (dias_no_periodo * peso_do_dia) * (tarefa.porcentagem / 100)

            pontos_finais = 0
            for user in usuarios:
                pontos_finais += verificarAtuacao(tarefa, user, peso_da_tarefa)

            retorno['pontos'] = pontos_finais
            return retorno

def CalcularPrevistoXRealizado(tarefa, data_inicio, data_fim, usuarios):
    retorno = {
        'processo' : tarefa.processo_relacionado,
        'realizado' : 0,
        'atraso' : 0,
        'impedimento' : 0
    }

    for user in usuarios:
        if tarefa.pendente_por == user:
            retorno['impedimento'] += 1

    if tarefa.stat == 'A fazer':
        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            return retorno

        else:
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa = dias_no_periodo * peso_do_dia

            atraso = 0
            for user in usuarios:
                atraso += verificarAtuacao(tarefa, user, peso_da_tarefa)
            
            retorno['atraso'] = atraso
            return retorno

    if tarefa.stat == 'Feito':
        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            return retorno

        else:
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa = dias_no_periodo * peso_do_dia

            pontos_finais = 0
            for user in usuarios:
                pontos_finais += verificarAtuacao(tarefa, user, peso_da_tarefa)
            
            retorno['realizado'] = pontos_finais
            return retorno
    
    if tarefa.stat == 'Fazendo':
        if date.today() < data_fim:
            tarefa.data_fim = date.today()
        else:
            tarefa.data_fim = data_fim

        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            return retorno
        else: 
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa_realizado = (dias_no_periodo * peso_do_dia) * (tarefa.porcentagem / 100)

            porcentagem_restante_tarefa = (100 - tarefa.porcentagem) / 100
            peso_da_tarefa_Arealizar = (dias_no_periodo * peso_do_dia) * porcentagem_restante_tarefa

            pontos_finais_realizado = 0
            pontos_finais_Arealizar = 0
            for user in usuarios:
                pontos_finais_realizado += verificarAtuacao(tarefa, user, peso_da_tarefa_realizado)
                pontos_finais_Arealizar += verificarAtuacao(tarefa, user, peso_da_tarefa_Arealizar)

            retorno['realizado'] = pontos_finais_realizado
            retorno['atraso'] = pontos_finais_Arealizar

            return retorno

def CalcularCC(tarefa, data_inicio, data_fim, usuarios):
    retorno = {
        'cc' : tarefa.centro_custo,
        'pontos' : 0
    }

    if tarefa.stat == 'A fazer':
        retorno['pontos'] = 0
        return retorno

    if tarefa.stat == 'Feito':
        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            retorno['pontos'] = 0
            return retorno
        else:
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa = dias_no_periodo * peso_do_dia

            pontos_finais = 0
            for user in usuarios:
                pontos_finais += verificarAtuacao(tarefa, user, peso_da_tarefa)
            
            retorno['pontos'] = pontos_finais
            return retorno
    
    if tarefa.stat == 'Fazendo':
        if date.today() < data_fim:
            tarefa.data_fim = date.today()
        else:
            tarefa.data_fim = data_fim

        dias_no_periodo = diasNoPeriodo(data_inicio, data_fim, tarefa)
        
        if dias_no_periodo == 0:
            retorno['pontos'] = 0
            return retorno
        else: 
            peso_do_dia = pesoDoDia(tarefa)

            peso_da_tarefa = (dias_no_periodo * peso_do_dia) * (tarefa.porcentagem / 100)

            pontos_finais = 0
            for user in usuarios:
                pontos_finais += verificarAtuacao(tarefa, user, peso_da_tarefa)

            retorno['pontos'] = pontos_finais
            return retorno

def gerarCor():
    cores_hex = [
        "#363636", 
        "#6A5ACD", "#000080", "#0000FF", "#4169E1", "#00BFFF",
        "#00FFFF", "#008B8B", "#7FFFD4",
        "#00FA9A", "#3CB371", "#006400", "#00FF00", "#9ACD32", "#808000",
        "#DAA520", "#8B4511", "#BC8F8F", "#D2691E", "#FFDEAD",
        "#7B68EE", "#4B0082", "#8B008B", "#FF00FF", 
        "#C71585", "#FF1493", "#DC143C	", 
        "#800000", "#B22222", "#FF0000",
        "#FF4500", "#FF8C00", "#FFA500",
        "#FFD700", "#FFFF00", "#F0E68C",
    ]

    return cores_hex[randint(0, len(cores_hex)-1)]