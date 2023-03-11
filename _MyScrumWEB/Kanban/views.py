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
from Tarefa.models import Tarefa, Executor
from Tarefa.forms import TarefaForms
from _Login.views import get_user
from Processo.models import Processos
from _MyScrumWEB import urls
from Etapa.models import Etapas
from Sub_etapa.models import SubEtapas

# Import de mesmo App
from .models import TarefasKanban

# Import Biblioteca Python
from datetime import date, datetime, timedelta
import json

# Create your views here.

@login_required(login_url=urls.getUrlSubdominio())
def kanban(request):
    usuario = get_user(request.user)

    tarefas = []
    filtros = {}
    filtrosHierarquia = ""
    filtrosCC = ""
    filtrosEtapa = ""
    filtrosSubEtapa = ""
    filtrosDPTO = ""
    filtrosProcesso = ""
    filtrosTarefaMae = ""
    filtrosAutoridade = ""
    filtrosResponsavel = ""
    filtrosPessoa = ""
    filtrosExecutor = ""
    filtrosImpedimento = ""
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

    ################------------------------------################
    ################ Filtro de Tarefa Mãe / Filho ################
    tarefasMae = request.GET.getlist('tarefa-mae')
    if len(tarefasMae):
        filtros['tarefaMae'] = tarefasMae
        tarefasMae = str(tarefasMae).replace('[','(').replace(']',')')
        
        auxiliarIdStatusMae = ''
        auxiliarIdStatusFilho = ''
        comparador1 = ''

        if 'Mãe' in tarefasMae:
            auxiliarIdStatusMae += 'id_status = 0 OR (processo_relacionado = "Processo Cível" AND id_status = 1)'
        if 'Filhos' in tarefasMae:
            auxiliarIdStatusFilho += '(processo_relacionado = "Processo Cível" AND id_status > 1) OR (processo_relacionado <> "Processo Cível" AND id_status >= 1)'

        if len(request.GET.getlist('tarefa-mae')) >= 2:
            comparador1 = 'OR'

        if 'Tarefas' in tarefasMae:
            if 'Mãe' in tarefasMae and 'Filhos' in tarefasMae:
                filtrosTarefaMae = ""
            elif 'Mãe' in tarefasMae:
                filtrosTarefaMae = f''' ({auxiliarIdStatusMae} OR id_status is null) AND '''
            else:
                filtrosTarefaMae = f''' ({auxiliarIdStatusFilho} {comparador1} id_status is null) AND '''
        else:
            filtrosTarefaMae = f'''({auxiliarIdStatusMae} {comparador1} {auxiliarIdStatusFilho}) AND '''
    ################ Filtro de Tarefa Mãe / Filho ################
    ################------------------------------################

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

    # #################--------------------############################
    # ################# Filtro de Empreendimento ##########################
    # empreendimentos = request.GET.getlist('empreendimento')
    # if len(empreendimentos):
    #     filtros['empreendimento'] = empreendimentos
    #     empreendimentos = str(empreendimentos).replace('[','(').replace(']',')')
    #     filtrosEmpreendimento = f''' empreendimento in {empreendimentos} AND '''
    # ################# Filtro de Autoridade ##########################
    # #################--------------------############################

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
    #################--------------------############################

    # is_staff = 0, Usuario = tem acesso apenas as tarefas onde contem o seu nome
    # is_staff = 1, Administrador = tem acesso a todas Tarefas
    # is_staff = 2, Lider = tem acessso as tarefas com seu nome e as tarefas do seu departamento
    # is_staff = 3, Gestor = tem acesso as tarefas com sue nome e as tarefas do seu centro custo

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
    {filtros5w2h}
    {filtrosTarefaMae}

    CASE 
        WHEN (stat = 'A fazer' or stat = 'A Fazer') and id_empresa = '{usuario.id_empresa}'
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim < '{data_inicio}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Feito' and id_empresa = '{usuario.id_empresa}'
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' OR
                data_fim BETWEEN '{data_inicio}' AND '{data_fim}' OR
                (data_ini < '{data_inicio}' AND data_fim > '{data_fim}')
        WHEN stat = 'Fazendo' and id_empresa = '{usuario.id_empresa}'
            THEN stat != 'Cancelado'
    END
    """

    tarefas = TarefasKanban.objects.extra(where=[WHERE]).order_by('prioridade')

    aFazer = []
    Fazendo = []
    Feito = []
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

    for tarefa in tarefas:
        try:
            if tarefa.id_status == 1 and tarefa.id_filho != '':
                tarefaMae = TarefasKanban.objects.get(pk = tarefa.id_filho)
                
                if(tarefaMae not in tarefas and 
                    tarefaMae not in aFazer and
                    tarefaMae not in Fazendo and
                    tarefaMae not in Feito
                ):
                    if tarefaMae.stat == 'A fazer' or tarefaMae.stat == 'A Fazer':
                        tarefaMae.data_ini = tarefaMae.data_ini.strftime('%d/%m/%Y')
                        tarefaMae.data_fim = tarefaMae.data_fim.strftime('%d/%m/%Y')
                        tarefaMae.Executores = getExecutores(tarefaMae)
                        aFazer.append(tarefaMae)
                    elif tarefaMae.stat == 'Fazendo':
                        tarefaMae.data_ini = tarefaMae.data_ini.strftime('%d/%m/%Y')
                        tarefaMae.data_fim = tarefaMae.data_fim.strftime('%d/%m/%Y')
                        tarefaMae.Executores = getExecutores(tarefaMae)
                        Fazendo.append(tarefaMae)
                    elif tarefaMae.stat == 'Feito':
                        tarefaMae.data_ini = tarefaMae.data_ini.strftime('%d/%m/%Y')
                        tarefaMae.data_fim = tarefaMae.data_fim.strftime('%d/%m/%Y')
                        tarefaMae.Executores = getExecutores(tarefaMae)
                        Feito.append(tarefaMae)
        except:
            None

        if tarefa.stat == 'A fazer' or tarefa.stat == 'A Fazer':
            tarefa.data_ini = tarefa.data_ini.strftime('%d/%m/%Y')
            tarefa.data_fim = tarefa.data_fim.strftime('%d/%m/%Y')
            tarefa.Executores = getExecutores(tarefa)
            aFazer.append(tarefa)
        elif tarefa.stat == 'Fazendo':
            tarefa.data_ini = tarefa.data_ini.strftime('%d/%m/%Y')
            tarefa.data_fim = tarefa.data_fim.strftime('%d/%m/%Y')
            tarefa.Executores = getExecutores(tarefa)
            Fazendo.append(tarefa)
        elif tarefa.stat == 'Feito':
            tarefa.data_ini = tarefa.data_ini.strftime('%d/%m/%Y')
            tarefa.data_fim = tarefa.data_fim.strftime('%d/%m/%Y')
            tarefa.Executores = getExecutores(tarefa)
            Feito.append(tarefa)

    context = {
        'aFazer' : aFazer,
        'Fazendo' : Fazendo,
        'Feito' : Feito,
        'pessoas' : pessoas,
        'departamentos' : departamentos,
        'centrocustos' : centrocustos,
        'etapas' : etapas,
        'subetapas' : subetapas,
        'processos' : processos,
        'filtros' : filtros,
        'r5w2hT' : r5w2hT,
        'usuario' : usuario,
        'form' : form
    }
 
    return render(request, 'kanban.html', context)

@csrf_exempt
def editarTarefa(request):
    if request.is_ajax() and request.POST:
        print('Editar a tarefa')
    else:
        raise Http404

def exibirTarefa(request, id):
    if request.method == 'GET' and request.is_ajax():

        # Buscando valores da tarefa
        tarefa = get_object_or_404(Tarefa, pk=id)

        tarefa.autoridade = Pessoa.objects.values('id_pessoa').get(nome=tarefa.autoridade)['id_pessoa']
        tarefa.responsavel = Pessoa.objects.values('id_pessoa').get(nome=tarefa.responsavel)['id_pessoa']

        try:
            tarefa.checado = Pessoa.objects.values('id_pessoa').get(nome=tarefa.checado)['id_pessoa']
        except:
            print('Checado não preenchido')

        try:
            tarefa.pendente_por = Pessoa.objects.values('id_pessoa').get(nome=tarefa.pendente_por)['id_pessoa']
        except:
            print('Pendência não preenchido')

        # Buscando Excutores da tarefa
        executores = get_object_or_404(Executor, id_tarefa=id)

        try:
            executores.executor1 = Pessoa.objects.values('id_pessoa').get(nome=executores.executor1)['id_pessoa']
        except:
            print('Campo não preenchido')
        try:
            executores.executor2 = Pessoa.objects.values('id_pessoa').get(nome=executores.executor2)['id_pessoa']
        except:
            print('Campo não preenchido')
        try:
            executores.executor3 = Pessoa.objects.values('id_pessoa').get(nome=executores.executor3)['id_pessoa']
        except:
            print('Campo não preenchido')
        try:
            executores.executor4 = Pessoa.objects.values('id_pessoa').get(nome=executores.executor4)['id_pessoa']
        except:
            print('Campo não preenchido')
        try:
            executores.executor5 = Pessoa.objects.values('id_pessoa').get(nome=executores.executor5)['id_pessoa']
        except:
            print('Campo não preenchido')
        try:
            executores.executor6 = Pessoa.objects.values('id_pessoa').get(nome=executores.executor6)['id_pessoa']
        except:
            print('Campo não preenchido')
        try:
            executores.executor7 = Pessoa.objects.values('id_pessoa').get(nome=executores.executor7)['id_pessoa']
        except:
            print('Campo não preenchido')
        try:
            executores.executor8 = Pessoa.objects.values('id_pessoa').get(nome=executores.executor8)['id_pessoa']
        except:
            print('Campo não preenchido')
        try:
            executores.executor9 = Pessoa.objects.values('id_pessoa').get(nome=executores.executor9)['id_pessoa']
        except:
            print('Campo não preenchido')
        try:
            executores.executor10 = Pessoa.objects.values('id_pessoa').get(nome=executores.executor10)['id_pessoa']
        except:
            print('Campo não preenchido')

        form = TarefaForms(instance=tarefa)
        executores_form = TarefaForms(instance=executores)

        context = {
            'form': form,
            'tarefa': tarefa,
            'executores_form': executores_form,
            }

        html_form = render_to_string('formTarefa.html',
            context,
            request=request,
        )
        
    return JsonResponse({'html_form': html_form})

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

    