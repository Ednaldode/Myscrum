# Import Django
from django.shortcuts import render
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required

# Import do mesmo App
from .models import TarefasHome

# Import de outros Apps
from _Login.models import Pessoa
from _Login.views import get_user
from Departamento.models import Departamento
from Centro_de_custo.models import CentroCusto
from Tamanho.models import Tamanho
from Feriado.models import Feriados
from _MyScrumWEB import urls
from Tarefa.views import gerarFiltros
from Tarefa.models import Tarefa

# Import Biblioteca Python
from datetime import date, datetime, timedelta
from random import randint


# Create your views here.

# Função que gera o  dashboard do usuario logado e os forms de filtros
@login_required(login_url=urls.getUrlSubdominio())
def dashboards(request):
    usuarios = Pessoa.objects.all()
    departamentos = Departamento.objects.all()
    centrocustos = CentroCusto.objects.all()

    usuario = get_user(request.user)
    nome_usuario = str(usuario.nome).replace(' ', '+')

    filtros = {}
    data_inicio = ''
    data_fim = ''

    if request.GET.get('start') != None and request.GET.get('end') != None :
        data_inicio = datetime.strptime(request.POST['start'], '%d/%m/%Y').date()
        data_fim = datetime.strptime(request.POST['end'], '%d/%m/%Y').date()

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

    WHERE = f"""
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
        WHEN stat = 'Cancelado'
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Fazendo'
            THEN
                id_tarefa != 0
    END
    """

    tarefas = TarefasHome.objects.extra(where=[WHERE])

    impedimentos = tarefas.filter(pendente_por=usuario.nome)
    impedimentos = len(impedimentos)

    WHERE = f"""
    '{usuario.nome}' in (responsavel, autoridade, checado, pendente_por, executor1, executor2, executor3, executor4, executor5, executor6, executor7, executor8,  executor9, executor10)
    """
    tarefas_filtradas = tarefas.extra(where=[WHERE])

    afazer = len(tarefas_filtradas.filter(stat='A fazer'))
    fazendo = len(tarefas_filtradas.filter(stat='Fazendo'))
    feito = len(tarefas_filtradas.filter(stat='Feito'))

    # ---------------------------- Graficos --------------------------------- #
    feriados = []
    feraidos_objects = Feriados.objects.filter(data_feriado__year=2020)
   
    for feriado in feraidos_objects:
        feriados.append(feriado.data_feriado)


    graficoProdutividade = {}
    graficoProdutividade['periodo'] = 0
    graficoProdutividade['previsto'] = 0
    graficoProdutividade['realizado'] = 0

    graficoProcedimento = {}
    graficoDemanda = {}
    graficoVelocimetro = {
        'pontos': 0,
        'dias_periodo': 0,
    }

    #Percorre as tarefas e chama as funções
    for tarefa in tarefas_filtradas:
        calcularGraficoProdutividade(tarefa, graficoProdutividade, usuario, data_inicio, data_fim, feriados)
        calcularGraficoProcedimento(tarefa, graficoProcedimento, usuario, data_inicio, data_fim, feriados)
        calcularGraficoDemanda(tarefa, graficoDemanda, usuario, data_inicio, data_fim, feriados)
        calcularGraficoVelocimetro(tarefa, graficoVelocimetro, usuario, data_inicio, data_fim, feriados)

    #Irá percorrer os dias do mês e faz a divisão da média tirando os feriados 
    while data_inicio <= date.today():
        if data_inicio not in feriados:
            graficoVelocimetro['dias_periodo'] += 1
        data_inicio = data_inicio + timedelta(days=1)
    
    graficoVelocimetro['pontos'] = graficoVelocimetro['pontos']/graficoVelocimetro['dias_periodo']

    dic = graficoProcedimento
    graficoProcedimento = {}
    graficoProcedimento['processos'] = []
    graficoProcedimento['realizado'] = []
    graficoProcedimento['atrasado'] = []
    graficoProcedimento['impedimento'] = []

    for key, value in dic.items():
        graficoProcedimento['processos'].append(key)
        graficoProcedimento['realizado'].append(str(round(value['realizado'],2)))
        graficoProcedimento['atrasado'].append(str(round(value['previsto'] - value['realizado'],2)))
        graficoProcedimento['impedimento'].append(str(value['impedimento']))

    dic = graficoDemanda
    graficoDemanda = {}
    graficoDemanda['processos'] = []
    graficoDemanda['realizado'] = []
    graficoDemanda['cores'] = []

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

    for key, value in dic.items():
        graficoDemanda['processos'].append(key)
        graficoDemanda['realizado'].append(str(round(value['realizado'],2)))
        graficoDemanda['cores'].append(cores_hex[randint(0, len(cores_hex)-1)])
    # ---------------------------- Graficos --------------------------------- #

    # --------------------- CONTEXT ----------------------- #
    context = {
        'afazer' : afazer,
        'fazendo' : fazendo,
        'feito' : feito,
        'impedimentos' : impedimentos,
        'usuario' : usuario,
        'departamentos' : departamentos,
        'centrocustos' : centrocustos,
        'nome_usuario' : nome_usuario,
        'filtros' : filtros,
        'graficoProdutividade' : graficoProdutividade,
        'graficoProcedimento' : graficoProcedimento,
        'graficoDemanda' : graficoDemanda,
        'graficoVelocimetro': graficoVelocimetro,
        'usuarios' : usuarios,
    }

    return render(request, 'dashboards.html', context)

@login_required(login_url=urls.getUrlSubdominio())
def home(request):
    usuario = get_user(request.user)
    nome_usuario = str(usuario.nome).replace(' ', '+')

    filtros = {}
    data_inicio = ''
    data_fim = ''

    if request.GET.get('start') != None and request.GET.get('end') != None :
        data_inicio = datetime.strptime(request.POST['start'], '%d/%m/%Y').date()
        data_fim = datetime.strptime(request.POST['end'], '%d/%m/%Y').date()

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

    WHERE = f"""
    CASE 
        WHEN stat = 'A fazer'
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Feito'
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Cancelado'
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Fazendo'
            THEN
                id_tarefa != 0
    END
    """

    tarefas = TarefasHome.objects.extra(where=[WHERE])

    impedimentos = tarefas.filter(pendente_por=usuario.nome)
    impedimentos = len(impedimentos)

    WHERE = f"""
    '{usuario.nome}' in (responsavel, autoridade, checado, pendente_por, executor1, executor2, executor3, executor4, executor5, executor6, executor7, executor8,  executor9, executor10)
    """
    tarefas_filtradas = tarefas.extra(where=[WHERE])

    afazer = len(tarefas_filtradas.filter(stat='A fazer'))
    fazendo = len(tarefas_filtradas.filter(stat='Fazendo'))
    feito = len(tarefas_filtradas.filter(stat='Feito'))

    # ---------------------------- Graficos --------------------------------- #
    feriados = []
    feraidos_objects = Feriados.objects.filter(data_feriado__year=2020)
   
    for feriado in feraidos_objects:
        feriados.append(feriado.data_feriado)


    graficoProdutividade = {}
    graficoProdutividade['periodo'] = 0
    graficoProdutividade['previsto'] = 0
    graficoProdutividade['realizado'] = 0

    graficoProcedimento = {}
    graficoDemanda = {}
    graficoVelocimetro = {
        'pontos': 0,
        'dias_periodo': 0,
    }

    #Percorre as tarefas e chama as funções
    for tarefa in tarefas_filtradas:
        calcularGraficoProdutividade(tarefa, graficoProdutividade, usuario, data_inicio, data_fim, feriados)
        calcularGraficoProcedimento(tarefa, graficoProcedimento, usuario, data_inicio, data_fim, feriados)
        calcularGraficoDemanda(tarefa, graficoDemanda, usuario, data_inicio, data_fim, feriados)
        calcularGraficoVelocimetro(tarefa, graficoVelocimetro, usuario, data_inicio, data_fim, feriados)

    #Irá percorrer os dias do mês e faz a divisão da média tirando os feriados 
    while data_inicio <= date.today():
        if data_inicio not in feriados:
            graficoVelocimetro['dias_periodo'] += 1
        data_inicio = data_inicio + timedelta(days=1)
    
    graficoVelocimetro['pontos'] = graficoVelocimetro['pontos']/graficoVelocimetro['dias_periodo']

    dic = graficoProcedimento
    graficoProcedimento = {}
    graficoProcedimento['processos'] = []
    graficoProcedimento['realizado'] = []
    graficoProcedimento['atrasado'] = []
    graficoProcedimento['impedimento'] = []

    for key, value in dic.items():
        graficoProcedimento['processos'].append(key)
        graficoProcedimento['realizado'].append(str(round(value['realizado'],2)))
        graficoProcedimento['atrasado'].append(str(round(value['previsto'] - value['realizado'],2)))
        graficoProcedimento['impedimento'].append(str(value['impedimento']))

    dic = graficoDemanda
    graficoDemanda = {}
    graficoDemanda['processos'] = []
    graficoDemanda['realizado'] = []
    graficoDemanda['cores'] = []

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

    for key, value in dic.items():
        graficoDemanda['processos'].append(key)
        graficoDemanda['realizado'].append(str(round(value['realizado'],2)))
        graficoDemanda['cores'].append(cores_hex[randint(0, len(cores_hex)-1)])
    # ---------------------------- Graficos --------------------------------- #

    # --------------------- CONTEXT ----------------------- #
    context = {
        'afazer' : afazer,
        'fazendo' : fazendo,
        'feito' : feito,
        'impedimentos' : impedimentos,
        'usuario' : usuario,
        'nome_usuario' : nome_usuario,
        'filtros' : filtros,
        'graficoProdutividade' : graficoProdutividade,
        'graficoProcedimento' : graficoProcedimento,
        'graficoDemanda' : graficoDemanda,
        'graficoVelocimetro': graficoVelocimetro,
    }

    return render(request, 'home.html', context)

# Função que gera os dashboards filtrados
@login_required(login_url=urls.getUrlSubdominio())
def dashboardResult(request):
    usuario = request.GET.getlist('usuarios')

    filtros = {}
    data_inicio = ''
    data_fim = ''
    filtrosDPTO = ''
    filtrosCC= ''
    
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

    
    #################--------------------##########################
    ################# Filtro de Centro de custo ###################
    # Se o campo centrocusto não estiver vazio filtra tarefas baseada no centrocusto de custo escolhido
    centro_custos = request.GET.getlist('ccs')
    if len(centro_custos) != 0 :
        centro_custos = str(centro_custos).replace('[','(').replace(']',')')
        filtrosCC = f''' centro_custo in {centro_custos} AND '''
    ################# Filtro de Centro de custo ###################
    #################--------------------##########################

    #################--------------------##########################
    ################# Filtro de Departamento ######################
    departamentos = request.GET.getlist('dptos')
    if len(departamentos) != 0 :
        departamentos = str(departamentos).replace('[','(').replace(']',')')
        filtrosDPTO = f''' departamento in {departamentos} AND '''
    ################# Filtro de Departamento ######################
    #################--------------------##########################


    WHERE = f"""
    {filtrosDPTO}
    {filtrosCC}
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
        WHEN stat = 'Cancelado'
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Fazendo'
            THEN
                id_tarefa != 0
    END
    """

    tarefas = TarefasHome.objects.extra(where=[WHERE])

    impedimentos = tarefas.filter(pendente_por__in=usuario)
    impedimentos = len(impedimentos)

    usuario.append('0')
    usuario_pesquisa = tuple(usuario)

    WHERE = f"""
        responsavel in {usuario_pesquisa} OR
        autoridade in {usuario_pesquisa} OR 
        checado in {usuario_pesquisa} OR
        pendente_por in {usuario_pesquisa} OR
        executor1 in {usuario_pesquisa} OR
        executor2 in {usuario_pesquisa} OR
        executor3 in {usuario_pesquisa} OR
        executor4 in {usuario_pesquisa} OR
        executor5 in {usuario_pesquisa} OR
        executor6 in {usuario_pesquisa} OR 
        executor7 in {usuario_pesquisa} OR 
        executor8 in {usuario_pesquisa} OR
        executor9 in {usuario_pesquisa} OR  
        executor10 in {usuario_pesquisa}
    """
    tarefas_filtradas = tarefas.extra(where=[WHERE])

    afazer = len(tarefas_filtradas.filter(stat='A fazer'))
    fazendo = len(tarefas_filtradas.filter(stat='Fazendo'))
    feito = len(tarefas_filtradas.filter(stat='Feito'))

    # ---------------------------- Graficos --------------------------------- #
    feriados = []
    feraidos_objects = Feriados.objects.filter(data_feriado__year=2020)
   
    for feriado in feraidos_objects:
        feriados.append(feriado.data_feriado)

    graficoProdutividade = {}
    graficoProdutividade['periodo'] = 0
    graficoProdutividade['previsto'] = 0
    graficoProdutividade['realizado'] = 0

    graficoProcedimento = {}
    graficoDemanda = {}
    graficoVelocimetro = {
        'pontos': 0,
        'dias_periodo': 0,
    }

    #Percorre os usuarios e filtra as tarefas, depois percorre as tarefas chamando as funções para calculos
    usuario.remove('0')
    for user in usuario:
        WHERE = f"""
        '{user}' in (responsavel, autoridade, checado, pendente_por, executor1, executor2, executor3, executor4, executor5, executor6, executor7, executor8,  executor9, executor10)
        """
        tarefas_filtradas = tarefas.extra(where=[WHERE])
        user = Pessoa.objects.get(nome=user)
        for tarefa in tarefas_filtradas:
            calcularGraficoProdutividade(tarefa, graficoProdutividade, user, data_inicio, data_fim, feriados)
            calcularGraficoProcedimento(tarefa, graficoProcedimento, user, data_inicio, data_fim, feriados)
            calcularGraficoDemanda(tarefa, graficoDemanda, user, data_inicio, data_fim, feriados)
            calcularGraficoVelocimetro(tarefa, graficoVelocimetro, user, data_inicio, data_fim, feriados)
            

    #Irá percorrer os dias do mês e faz a divisão da média tirando os feriados 
    while data_inicio <= date.today():
        if data_inicio not in feriados:
            graficoVelocimetro['dias_periodo'] += 1
        data_inicio = data_inicio + timedelta(days=1)
    
    graficoVelocimetro['pontos'] = graficoVelocimetro['pontos']/graficoVelocimetro['dias_periodo']

    dic = graficoProcedimento
    graficoProcedimento = {}
    graficoProcedimento['processos'] = []
    graficoProcedimento['realizado'] = []
    graficoProcedimento['atrasado'] = []
    graficoProcedimento['impedimento'] = []

    for key, value in dic.items():
        graficoProcedimento['processos'].append(key)
        graficoProcedimento['realizado'].append(str(round(value['realizado'],2)))
        graficoProcedimento['atrasado'].append(str(round(value['previsto'] - value['realizado'],2)))
        graficoProcedimento['impedimento'].append(str(value['impedimento']))

    dic = graficoDemanda
    graficoDemanda = {}
    graficoDemanda['processos'] = []
    graficoDemanda['realizado'] = []
    graficoDemanda['cores'] = []

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

    for key, value in dic.items():
        graficoDemanda['processos'].append(key)
        graficoDemanda['realizado'].append(str(round(value['realizado'],2)))
        graficoDemanda['cores'].append(cores_hex[randint(0, len(cores_hex)-1)])
    # ---------------------------- Graficos --------------------------------- #


    # --------------------- CONTEXT ----------------------- #
    context = {
        'afazer' : afazer,
        'fazendo' : fazendo,
        'feito' : feito,
        'impedimentos' : impedimentos,
        'usuario' : usuario,
        'filtros' : filtros,
        'graficoProdutividade' : graficoProdutividade,
        'graficoProcedimento' : graficoProcedimento,
        'graficoDemanda' : graficoDemanda,
        'graficoVelocimetro': graficoVelocimetro,
    }

    if len(usuario) == 1:
        user = Pessoa.objects.get(nome=usuario[0])
        usuario = get_user(user.id_user)
        context['usuario'] = usuario
        nome_usuario = str(usuario.nome).replace(' ', '+')
        context['nome_usuario'] = nome_usuario

    return render(request, "dashboardResult.html", context)

def calcularGraficoProdutividade(tarefa, graficoProdutividade, usuario, data_inicio, data_fim, feriados):
    
    graficoProdutividade['periodo'] = float(graficoProdutividade['periodo'])
    graficoProdutividade['previsto'] = float(graficoProdutividade['previsto'])
    graficoProdutividade['realizado'] = float(graficoProdutividade['realizado'])

    if graficoProdutividade['periodo'] == 0:
        # -------- Calculo de periodo -----------#
        hoje = date.today()
        data = date(hoje.year, hoje.month, 1 )

        # Calculo de periodo #
        while data <= hoje :
            if data.weekday() in [0,1,2,3,4]:
                graficoProdutividade['periodo'] += 8

            data = data + timedelta(days=1)
        # -------- Calculo de periodo -----------#

    # Calculo realizado e previsto #
    periodo_inicio = data_inicio
    periodo_fim = data_fim

    dias_nao_uteis = feriados
    dias_dentro_periodo = 0
    dias_uteis_tarefa = 0

    inicio = tarefa.data_ini
    fim = tarefa.data_fim

    # Enquanto o inicio da tarefa for diferente do final proseguimos
    while inicio <= fim:

        # Se o dia em decorrencia for dia util adicionamos mais 1 aos dias uteis da tarefa
        if inicio not in dias_nao_uteis:
            dias_uteis_tarefa += 1
            # Se o dia em decorrencia estiver dentro do periodo pesquisado adicionamos mais 1 aos dias dentro do periodo
            if inicio >= periodo_inicio and inicio <= periodo_fim:
                dias_dentro_periodo += 1

        inicio = inicio + timedelta(days=1)
    if dias_uteis_tarefa != 0:
        if tarefa.stat == 'A fazer':
             pontos = (tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo
        elif tarefa.stat == 'Feito' or tarefa.stat == 'Fazendo':
            pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
        else:
            pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
    else:
        pontos = 0  

    # verificando se o usuario consta como autoridade ou responsavel na tarefa
    if tarefa.autoridade == usuario.nome:
        if tarefa.stat != 'A fazer':
            graficoProdutividade['realizado'] += pontos * 0.05
        graficoProdutividade['previsto'] += pontos * 0.05
    if tarefa.responsavel == usuario.nome:
        if tarefa.stat != 'A fazer':
            graficoProdutividade['realizado'] += pontos * 0.15
        graficoProdutividade['previsto'] += pontos * 0.15
    
    # verificando se o usuario consta como executor da tarefa
    # print("Tarefa: ", tarefa.id_tarefa, "Porcento1: ", tarefa.executor1, tarefa.porcento1, "Porcento2: ", tarefa.executor2, tarefa.porcento2, "Porcento3: ", tarefa.executor3, tarefa.porcento3, "Porcento4: ", tarefa.executor4, tarefa.porcento4, "Porcento5: ", tarefa.executor5, tarefa.porcento5, "Porcento6: ", tarefa.executor6, tarefa.porcento6, "Porcento7: ", tarefa.executor7, tarefa.porcento7, "Porcento8: ", tarefa.executor8, tarefa.porcento8, "Porcento9: ", tarefa.executor9, tarefa.porcento9, "Porcento10: ", tarefa.executor10, tarefa.porcento10)
    if tarefa.executor1 == usuario.nome:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento1 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento1 / 100)
    
    elif tarefa.executor2 == usuario.nome:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento2 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento2 / 100)
    
    elif tarefa.executor3 == usuario.nome:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento3 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento3 / 100)
    
    elif tarefa.executor4 == usuario.nome:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento4 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento4 / 100)
    
    elif tarefa.executor5 == usuario.nome:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento5 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento5 / 100)
    
    elif tarefa.executor6 == usuario.nome:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento6 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento6 / 100)

    elif tarefa.executor7 == usuario.nome:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento7 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento7 / 100)

    elif tarefa.executor8 == usuario.nome:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento8 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento8 / 100)

    elif tarefa.executor9 == usuario.nome:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento9 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento9 / 100)

    elif tarefa.executor10 == usuario.nome:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento10 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento10 / 100)
            
    # ---------------- # 
    graficoProdutividade['periodo'] = str(round(graficoProdutividade['periodo'],2))
    graficoProdutividade['previsto'] = str(round(graficoProdutividade['previsto'],2))
    graficoProdutividade['realizado'] = str(round(graficoProdutividade['realizado'],2))
    
    return None

def calcularGraficoVelocimetro(tarefa, graficoVelocimetro, usuario, data_inicio, data_fim, feriados):
    
    peso = tarefa.tamanho
    inicio_tarefa = tarefa.data_ini
    fim_tarefa = tarefa.data_fim
    inicio_periodo = data_inicio
    fim_periodo = data_fim
    dias_uteis_tarefa = 0
    dias_dentro_periodo = 0
    pontos_finais = 0

    if tarefa.stat == 'Feito':
        qtd_dias = fim_tarefa - inicio_tarefa
        qtd_dias = qtd_dias + timedelta(days=1)


        while inicio_tarefa <= fim_tarefa:
            if inicio_tarefa not in feriados:
                dias_uteis_tarefa += 1
                if inicio_tarefa >= inicio_periodo and inicio_tarefa <= fim_periodo:
                    dias_dentro_periodo +=1
            #Timedelta incrementa 1 dia na data
            inicio_tarefa = inicio_tarefa + timedelta(days=1)
        
        #-----Cálculos-----#
        #Quanto a tarefa vale
        if int(qtd_dias.days) == 0:
            qtd_dias.days = 1
        peso_util = (peso/int(qtd_dias.days)) * dias_uteis_tarefa

        if tarefa.autoridade == usuario.nome:
            pontos_finais += peso_util * 0.05

        if tarefa.responsavel == usuario.nome:
            pontos_finais += peso_util * 0.15
        
        if tarefa.executor1 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento1/100)
        if tarefa.executor2 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento2/100)
        if tarefa.executor3 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento3/100)
        if tarefa.executor4 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento4/100)
        if tarefa.executor5 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento5/100)
        if tarefa.executor6 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento6/100)
        if tarefa.executor7 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento7/100)
        if tarefa.executor8 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento8/100)
        if tarefa.executor9 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento9/100)
        if tarefa.executor10 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento10/100)

        #Divide a pontuação pela quantidade de dias do período decorridos até hoje gerando a pontuação média do usuário
        graficoVelocimetro['pontos'] += pontos_finais

    elif tarefa.stat == 'Fazendo':
        qtd_dias = fim_tarefa - inicio_tarefa
        qtd_dias = qtd_dias + timedelta(days=1)

        while inicio_tarefa <= date.today():
            if inicio_tarefa not in feriados:
                dias_uteis_tarefa += 1
                if inicio_tarefa >= inicio_periodo and inicio_tarefa <= fim_periodo:
                    dias_dentro_periodo +=1
            #Timedelta incrementa 1 dia na data
            inicio_tarefa = inicio_tarefa + timedelta(days=1)
        
        if int(qtd_dias.days) == 0:
            qtd_dias.days = 1
        peso_util = peso*(tarefa.porcentagem/100)/int(qtd_dias.days)*dias_uteis_tarefa

        if tarefa.autoridade == usuario.nome:
            pontos_finais += peso_util * 0.05

        if tarefa.responsavel == usuario.nome:
            pontos_finais += peso_util * 0.15
        
        if tarefa.executor1 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento1/100)
        if tarefa.executor2 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento2/100)
        if tarefa.executor3 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento3/100)
        if tarefa.executor4 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento4/100)
        if tarefa.executor5 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento5/100)
        if tarefa.executor6 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento6/100)
        if tarefa.executor7 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento7/100)
        if tarefa.executor8 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento8/100)
        if tarefa.executor9 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento9/100)
        if tarefa.executor10 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento10/100)

        #Divide a pontuação pela quantidade de dias do período decorridos até hoje gerando a pontuação média do usuário
        graficoVelocimetro['pontos'] += pontos_finais
    
    else:
        return None

def calcularGraficoProcedimento(tarefa, graficoProcedimento, usuario, data_inicio, data_fim, feriados):
    # Se o nome do usuario constar na tarefa e tivermos criado a chave para o processo no dicionario criamos uma nova chave
    if usuario.nome in [tarefa.autoridade, tarefa.responsavel, tarefa.executor1, tarefa.executor2, tarefa.executor3, tarefa.executor4, tarefa.executor5, tarefa.executor6, tarefa.executor7, tarefa.executor8, tarefa.executor9, tarefa.executor10, tarefa.pendente_por] and tarefa.processo_relacionado != None:
        if tarefa.processo_relacionado not in graficoProcedimento:
            graficoProcedimento[tarefa.processo_relacionado] = {
                'realizado' : 0,
                'atraso' : 0,
                'impedimento' : 0,
                'previsto' : 0,
            }

        if tarefa.pendente_por == usuario.nome and tarefa.processo_relacionado != None:
            graficoProcedimento[tarefa.processo_relacionado]['impedimento'] += 1

        periodo_inicio = data_inicio
        periodo_fim = data_fim

        dias_nao_uteis = feriados
        dias_dentro_periodo = 0
        dias_uteis_tarefa = 0

        inicio = tarefa.data_ini
        fim = tarefa.data_fim

        # Enquanto o inicio da tarefa for diferente do final proseguimos
        while inicio <= fim:

            # Se o dia em decorrencia for dia util adicionamos mais 1 aos dias uteis da tarefa
            if inicio not in dias_nao_uteis:
                dias_uteis_tarefa += 1
                # Se o dia em decorrencia estiver dentro do periodo pesquisado adicionamos mais 1 aos dias dentro do periodo
                if inicio >= periodo_inicio and inicio <= periodo_fim:
                    dias_dentro_periodo += 1

            inicio = inicio + timedelta(days=1)
        if dias_uteis_tarefa != 0:
            if tarefa.stat == 'A fazer':
                pontos = (tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo
            elif tarefa.stat == 'Feito' or tarefa.stat == 'Fazendo':
                pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
            else: 
                pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
        else:
            pontos = 0  

        # verificando se o usuario consta como autoridade ou responsavel na tarefa
        if tarefa.autoridade == usuario.nome:
            if tarefa.stat != 'A fazer':
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += pontos * 0.05
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += pontos * 0.05
        if tarefa.responsavel == usuario.nome:
            if tarefa.stat != 'A fazer':
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += pontos * 0.15
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += pontos * 0.15
        
        # verificando se o usuario consta como executor da tarefa
        if tarefa.executor1 == usuario.nome:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento1 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento1 / 100)) * 0.80
        
        elif tarefa.executor2 == usuario.nome:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento2 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento2 / 100)) * 0.80
        
        elif tarefa.executor3 == usuario.nome:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento3 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento3 / 100)) * 0.80
        
        elif tarefa.executor4 == usuario.nome:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento4 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] +=(pontos * (tarefa.porcento4 / 100)) * 0.80
        
        elif tarefa.executor5 == usuario.nome:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento5 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento5 / 100)) * 0.80
        
        elif tarefa.executor6 == usuario.nome:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento6 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento6 / 100)) * 0.80

        elif tarefa.executor7 == usuario.nome:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento7 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento7 / 100)) * 0.80

        elif tarefa.executor8 == usuario.nome:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento8 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento8 / 100)) * 0.80

        elif tarefa.executor9 == usuario.nome:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento9 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento9 / 100)) * 0.80

        elif tarefa.executor10 == usuario.nome:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento10 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento10 / 100)) * 0.80

    return None

def calcularGraficoDemanda(tarefa, graficoProcedimento, usuario, data_inicio, data_fim, feriados):
    # Se o nome do usuario constar na tarefa e tivermos criado a chave para o processo no dicionario criamos uma nova chave
    if usuario.nome in [tarefa.autoridade, tarefa.responsavel, tarefa.executor1, tarefa.executor2, tarefa.executor3, tarefa.executor4, tarefa.executor5, tarefa.executor6, tarefa.executor7, tarefa.executor8, tarefa.executor9, tarefa.executor10] and tarefa.processo_relacionado != None:
        if tarefa.processo_relacionado not in graficoProcedimento:
            graficoProcedimento[tarefa.processo_relacionado] = {
                'realizado' : 0,
            }

        periodo_inicio = data_inicio
        periodo_fim = data_fim

        dias_nao_uteis = feriados
        dias_dentro_periodo = 0
        dias_uteis_tarefa = 0

        inicio = tarefa.data_ini
        fim = tarefa.data_fim

        # Enquanto o inicio da tarefa for diferente do final proseguimos
        while inicio <= fim:

            # Se o dia em decorrencia for dia util adicionamos mais 1 aos dias uteis da tarefa
            if inicio not in dias_nao_uteis:
                dias_uteis_tarefa += 1
                # Se o dia em decorrencia estiver dentro do periodo pesquisado adicionamos mais 1 aos dias dentro do periodo
                if inicio >= periodo_inicio and inicio <= periodo_fim:
                    dias_dentro_periodo += 1

            inicio = inicio + timedelta(days=1)
        if dias_uteis_tarefa != 0:
            if tarefa.stat == 'A fazer':
                pontos = (tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo
            elif tarefa.stat == 'Feito' or tarefa.stat == 'Fazendo':
                pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
            else: 
                pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
        else:
            pontos = 0  

        # verificando se o usuario consta como autoridade ou responsavel na tarefa
        if tarefa.autoridade == usuario.nome:
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += pontos * 0.05

        if tarefa.responsavel == usuario.nome:
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += pontos * 0.15
        
        # verificando se o usuario consta como executor da tarefa
        if tarefa.executor1 == usuario.nome:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento1 / 100)) * 0.80
        
        elif tarefa.executor2 == usuario.nome:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] +=(pontos * (tarefa.porcento2 / 100)) * 0.80
        
        elif tarefa.executor3 == usuario.nome:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento3 / 100)) * 0.80
        
        elif tarefa.executor4 == usuario.nome:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento4 / 100)) * 0.80
        
        elif tarefa.executor5 == usuario.nome:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento5 / 100)) * 0.80
        
        elif tarefa.executor6 == usuario.nome:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento6 / 100)) * 0.80

        elif tarefa.executor7 == usuario.nome:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento7 / 100)) * 0.80

        elif tarefa.executor8 == usuario.nome:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento8 / 100)) * 0.80

        elif tarefa.executor9 == usuario.nome:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento9 / 100)) * 0.80

        elif tarefa.executor10 == usuario.nome:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento10 / 100)) * 0.80

    return None

def calcularGraficoProdutividadeUsuarios(tarefa, graficoProdutividade, usuario, data_inicio, data_fim, feriados):
    
    graficoProdutividade['periodo'] = float(graficoProdutividade['periodo'])
    graficoProdutividade['previsto'] = float(graficoProdutividade['previsto'])
    graficoProdutividade['realizado'] = float(graficoProdutividade['realizado'])

    if graficoProdutividade['periodo'] == 0:
        # -------- Calculo de periodo -----------#
        hoje = date.today()
        data = date(hoje.year, hoje.month, 1 )

        # Calculo de periodo #
        while data <= hoje :
            if data.weekday() in [0,1,2,3,4]:
                graficoProdutividade['periodo'] += 8

            data = data + timedelta(days=1)
        # -------- Calculo de periodo -----------#

    # Calculo realizado e previsto #
    periodo_inicio = data_inicio
    periodo_fim = data_fim

    dias_nao_uteis = feriados
    dias_dentro_periodo = 0
    dias_uteis_tarefa = 0

    inicio = tarefa.data_ini
    fim = tarefa.data_fim

    # Enquanto o inicio da tarefa for diferente do final proseguimos
    while inicio <= fim:

        # Se o dia em decorrencia for dia util adicionamos mais 1 aos dias uteis da tarefa
        if inicio not in dias_nao_uteis:
            dias_uteis_tarefa += 1
            # Se o dia em decorrencia estiver dentro do periodo pesquisado adicionamos mais 1 aos dias dentro do periodo
            if inicio >= periodo_inicio and inicio <= periodo_fim:
                dias_dentro_periodo += 1

        inicio = inicio + timedelta(days=1)
    if dias_uteis_tarefa != 0:
        if tarefa.stat == 'A fazer':
             pontos = (tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo
        elif tarefa.stat == 'Feito' or tarefa.stat == 'Fazendo':
            pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
        else:
            pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
    else:
        pontos = 0  

    # verificando se o usuario consta como autoridade ou responsavel na tarefa
    if tarefa.autoridade == usuario:
        if tarefa.stat != 'A fazer':
            graficoProdutividade['realizado'] += pontos * 0.05
        graficoProdutividade['previsto'] += pontos * 0.05
    if tarefa.responsavel == usuario:
        if tarefa.stat != 'A fazer':
            graficoProdutividade['realizado'] += pontos * 0.15
        graficoProdutividade['previsto'] += pontos * 0.15
    
    # verificando se o usuario consta como executor da tarefa
    # print("Tarefa: ", tarefa.id_tarefa, "Porcento1: ", tarefa.executor1, tarefa.porcento1, "Porcento2: ", tarefa.executor2, tarefa.porcento2, "Porcento3: ", tarefa.executor3, tarefa.porcento3, "Porcento4: ", tarefa.executor4, tarefa.porcento4, "Porcento5: ", tarefa.executor5, tarefa.porcento5, "Porcento6: ", tarefa.executor6, tarefa.porcento6, "Porcento7: ", tarefa.executor7, tarefa.porcento7, "Porcento8: ", tarefa.executor8, tarefa.porcento8, "Porcento9: ", tarefa.executor9, tarefa.porcento9, "Porcento10: ", tarefa.executor10, tarefa.porcento10)
    if tarefa.executor1 == usuario:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento1 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento1 / 100)
    
    elif tarefa.executor2 == usuario:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento2 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento2 / 100)
    
    elif tarefa.executor3 == usuario:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento3 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento3 / 100)
    
    elif tarefa.executor4 == usuario:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento4 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento4 / 100)
    
    elif tarefa.executor5 == usuario:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento5 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento5 / 100)
    
    elif tarefa.executor6 == usuario:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento6 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento6 / 100)

    elif tarefa.executor7 == usuario:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento7 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento7 / 100)

    elif tarefa.executor8 == usuario:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento8 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento8 / 100)

    elif tarefa.executor9 == usuario:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento9 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento9 / 100)

    elif tarefa.executor10 == usuario:  
        if tarefa.stat != 'A fazer':      
            graficoProdutividade['realizado'] += pontos * 0.80 * (tarefa.porcento10 / 100)
        graficoProdutividade['previsto'] += pontos * 0.80 * (tarefa.porcento10 / 100)
            
    # ---------------- # 
    graficoProdutividade['periodo'] = str(round(graficoProdutividade['periodo'],2))
    graficoProdutividade['previsto'] = str(round(graficoProdutividade['previsto'],2))
    graficoProdutividade['realizado'] = str(round(graficoProdutividade['realizado'],2))
    
    return None

def calcularGraficoVelocimetroUsuarios(tarefa, graficoVelocimetro, usuario, data_inicio, data_fim, feriados):
    
    peso = tarefa.tamanho
    inicio_tarefa = tarefa.data_ini
    fim_tarefa = tarefa.data_fim
    inicio_periodo = data_inicio
    fim_periodo = data_fim
    dias_uteis_tarefa = 0
    dias_dentro_periodo = 0
    pontos_finais = 0

    if tarefa.stat == 'Feito':
        qtd_dias = fim_tarefa - inicio_tarefa
        qtd_dias = qtd_dias + timedelta(days=1)


        while inicio_tarefa <= fim_tarefa:
            if inicio_tarefa not in feriados:
                dias_uteis_tarefa += 1
                if inicio_tarefa >= inicio_periodo and inicio_tarefa <= fim_periodo:
                    dias_dentro_periodo +=1
            #Timedelta incrementa 1 dia na data
            inicio_tarefa = inicio_tarefa + timedelta(days=1)
        
        #-----Cálculos-----#
        #Quanto a tarefa vale
        if int(qtd_dias.days) == 0:
            qtd_dias.days = 1
        peso_util = (peso/int(qtd_dias.days)) * dias_uteis_tarefa

        if tarefa.autoridade == usuario.nome:
            pontos_finais += peso_util * 0.05

        if tarefa.responsavel == usuario.nome:
            pontos_finais += peso_util * 0.15
        
        if tarefa.executor1 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento1/100)
        if tarefa.executor2 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento2/100)
        if tarefa.executor3 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento3/100)
        if tarefa.executor4 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento4/100)
        if tarefa.executor5 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento5/100)
        if tarefa.executor6 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento6/100)
        if tarefa.executor7 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento7/100)
        if tarefa.executor8 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento8/100)
        if tarefa.executor9 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento9/100)
        if tarefa.executor10 == usuario.nome:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento10/100)

        #Divide a pontuação pela quantidade de dias do período decorridos até hoje gerando a pontuação média do usuário
        graficoVelocimetro['pontos'] += pontos_finais

    elif tarefa.stat == 'Fazendo':
        qtd_dias = fim_tarefa - inicio_tarefa
        qtd_dias = qtd_dias + timedelta(days=1)

        while inicio_tarefa <= date.today():
            if inicio_tarefa not in feriados:
                dias_uteis_tarefa += 1
                if inicio_tarefa >= inicio_periodo and inicio_tarefa <= fim_periodo:
                    dias_dentro_periodo +=1
            #Timedelta incrementa 1 dia na data
            inicio_tarefa = inicio_tarefa + timedelta(days=1)
        
        if int(qtd_dias.days) == 0:
            qtd_dias.days = 1
        peso_util = peso*(tarefa.porcentagem/100)/int(qtd_dias.days)*dias_uteis_tarefa

        if tarefa.autoridade == usuario:
            pontos_finais += peso_util * 0.05

        if tarefa.responsavel == usuario:
            pontos_finais += peso_util * 0.15
        
        if tarefa.executor1 == usuario:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento1/100)
        if tarefa.executor2 == usuario:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento2/100)
        if tarefa.executor3 == usuario:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento3/100)
        if tarefa.executor4 == usuario:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento4/100)
        if tarefa.executor5 == usuario:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento5/100)
        if tarefa.executor6 == usuario:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento6/100)
        if tarefa.executor7 == usuario:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento7/100)
        if tarefa.executor8 == usuario:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento8/100)
        if tarefa.executor9 == usuario:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento9/100)
        if tarefa.executor10 == usuario:
            pontos_finais += (peso_util * 0.8) * (tarefa.porcento10/100)

        #Divide a pontuação pela quantidade de dias do período decorridos até hoje gerando a pontuação média do usuário
        graficoVelocimetro['pontos'] += pontos_finais
    
    else:
        print("Tarefa não utilizavel")

def calcularGraficoProcedimentoUsuarios(tarefa, graficoProcedimento, usuario, data_inicio, data_fim, feriados):
    # Se o nome do usuario constar na tarefa e tivermos criado a chave para o processo no dicionario criamos uma nova chave
    if usuario in [tarefa.autoridade, tarefa.responsavel, tarefa.executor1, tarefa.executor2, tarefa.executor3, tarefa.executor4, tarefa.executor5, tarefa.executor6, tarefa.executor7, tarefa.executor8, tarefa.executor9, tarefa.executor10, tarefa.pendente_por] and tarefa.processo_relacionado != None:
        if tarefa.processo_relacionado not in graficoProcedimento:
            graficoProcedimento[tarefa.processo_relacionado] = {
                'realizado' : 0,
                'atraso' : 0,
                'impedimento' : 0,
                'previsto' : 0,
            }

        if tarefa.pendente_por == usuario and tarefa.processo_relacionado != None:
            graficoProcedimento[tarefa.processo_relacionado]['impedimento'] += 1

        periodo_inicio = data_inicio
        periodo_fim = data_fim

        dias_nao_uteis = feriados
        dias_dentro_periodo = 0
        dias_uteis_tarefa = 0

        inicio = tarefa.data_ini
        fim = tarefa.data_fim

        # Enquanto o inicio da tarefa for diferente do final proseguimos
        while inicio <= fim:

            # Se o dia em decorrencia for dia util adicionamos mais 1 aos dias uteis da tarefa
            if inicio not in dias_nao_uteis:
                dias_uteis_tarefa += 1
                # Se o dia em decorrencia estiver dentro do periodo pesquisado adicionamos mais 1 aos dias dentro do periodo
                if inicio >= periodo_inicio and inicio <= periodo_fim:
                    dias_dentro_periodo += 1

            inicio = inicio + timedelta(days=1)
        if dias_uteis_tarefa != 0:
            if tarefa.stat == 'A fazer':
                pontos = (tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo
            elif tarefa.stat == 'Feito' or tarefa.stat == 'Fazendo':
                pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
            else:
                pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
        else:
            pontos = 0  

        # verificando se o usuario consta como autoridade ou responsavel na tarefa
        if tarefa.autoridade == usuario:
            if tarefa.stat != 'A fazer':
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += pontos * 0.05
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += pontos * 0.05
        if tarefa.responsavel == usuario:
            if tarefa.stat != 'A fazer':
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += pontos * 0.15
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += pontos * 0.15
        
        # verificando se o usuario consta como executor da tarefa
        if tarefa.executor1 == usuario:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento1 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento1 / 100)) * 0.80
        
        elif tarefa.executor2 == usuario:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento2 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento2 / 100)) * 0.80
        
        elif tarefa.executor3 == usuario:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento3 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento3 / 100)) * 0.80
        
        elif tarefa.executor4 == usuario:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento4 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] +=(pontos * (tarefa.porcento4 / 100)) * 0.80
        
        elif tarefa.executor5 == usuario:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento5 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento5 / 100)) * 0.80
        
        elif tarefa.executor6 == usuario:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento6 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento6 / 100)) * 0.80

        elif tarefa.executor7 == usuario:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento7 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento7 / 100)) * 0.80

        elif tarefa.executor8 == usuario:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento8 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento8 / 100)) * 0.80

        elif tarefa.executor9 == usuario:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento9 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento9 / 100)) * 0.80

        elif tarefa.executor10 == usuario:  
            if tarefa.stat != 'A fazer':      
                graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento10 / 100)) * 0.80
            graficoProcedimento[tarefa.processo_relacionado]['previsto'] += (pontos * (tarefa.porcento10 / 100)) * 0.80

    return None

def calcularGraficoDemandaUsuarios(tarefa, graficoProcedimento, usuario, data_inicio, data_fim, feriados):
    # Se o nome do usuario constar na tarefa e tivermos criado a chave para o processo no dicionario criamos uma nova chave
    if usuario in [tarefa.autoridade, tarefa.responsavel, tarefa.executor1, tarefa.executor2, tarefa.executor3, tarefa.executor4, tarefa.executor5, tarefa.executor6, tarefa.executor7, tarefa.executor8, tarefa.executor9, tarefa.executor10] and tarefa.processo_relacionado != None:
        if tarefa.processo_relacionado not in graficoProcedimento:
            graficoProcedimento[tarefa.processo_relacionado] = {
                'realizado' : 0,
            }

        periodo_inicio = data_inicio
        periodo_fim = data_fim

        dias_nao_uteis = feriados
        dias_dentro_periodo = 0
        dias_uteis_tarefa = 0

        inicio = tarefa.data_ini
        fim = tarefa.data_fim

        # Enquanto o inicio da tarefa for diferente do final proseguimos
        while inicio <= fim:

            # Se o dia em decorrencia for dia util adicionamos mais 1 aos dias uteis da tarefa
            if inicio not in dias_nao_uteis:
                dias_uteis_tarefa += 1
                # Se o dia em decorrencia estiver dentro do periodo pesquisado adicionamos mais 1 aos dias dentro do periodo
                if inicio >= periodo_inicio and inicio <= periodo_fim:
                    dias_dentro_periodo += 1

            inicio = inicio + timedelta(days=1)
        if dias_uteis_tarefa != 0:
            if tarefa.stat == 'A fazer':
                pontos = (tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo
            elif tarefa.stat == 'Feito' or tarefa.stat == 'Fazendo':
                pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
            else:
                pontos = ((tarefa.tamanho / dias_uteis_tarefa) * dias_dentro_periodo) * (tarefa.porcentagem / 100)
        else:
            pontos = 0  

        # verificando se o usuario consta como autoridade ou responsavel na tarefa
        if tarefa.autoridade == usuario:
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += pontos * 0.05

        if tarefa.responsavel == usuario:
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += pontos * 0.15
        
        # verificando se o usuario consta como executor da tarefa
        if tarefa.executor1 == usuario:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento1 / 100)) * 0.80
        
        elif tarefa.executor2 == usuario:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] +=(pontos * (tarefa.porcento2 / 100)) * 0.80
        
        elif tarefa.executor3 == usuario:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento3 / 100)) * 0.80
        
        elif tarefa.executor4 == usuario:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento4 / 100)) * 0.80
        
        elif tarefa.executor5 == usuario:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento5 / 100)) * 0.80
        
        elif tarefa.executor6 == usuario:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento6 / 100)) * 0.80

        elif tarefa.executor7 == usuario:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento7 / 100)) * 0.80

        elif tarefa.executor8 == usuario:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento8 / 100)) * 0.80

        elif tarefa.executor9 == usuario:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento9 / 100)) * 0.80

        elif tarefa.executor10 == usuario:  
            graficoProcedimento[tarefa.processo_relacionado]['realizado'] += (pontos * (tarefa.porcento10 / 100)) * 0.80

    return None
