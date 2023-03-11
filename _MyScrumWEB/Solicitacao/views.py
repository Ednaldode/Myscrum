# Import Django
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage, File 

# Import de outros Apps
from _Login.models import Pessoa, Vinculos
from _Login.views import get_user
from _MyScrumWEB import urls
from Centro_de_custo.models import CentroCusto
from Departamento.models import Departamento
from Processo.models import Processos
from Tarefa.models import Tarefa, Executor
from Tarefa.forms import ExecutorFormsEditar
from Tarefa.views import editarTarefas

# Import de mesmo App
from .models import Solicitacao, Problema, ListarSolicitacoes, ExportarSolicitacoes, DashboardSAT
from .forms import SolicitacaoForms, ImpressaoForms, ExecutorForms, ListarForms, DashboardsForms

# Import Biblioteca Python
from datetime import date, datetime, timedelta
import json
import xlrd
import xlwt
import os

# Create your views here.

@login_required(login_url='/account/login')
def solicitacao(request):
    return render(request, 'solicitacao.html', context)

@login_required(login_url='/account/login')
def listar(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    solicitacoes = ListarSolicitacoes.objects.extra(where=[filtrosWhere['WHERE']]).order_by('prioridade')
    solicitacoesGeral = ListarSolicitacoes.objects.all()

    pessoas = Pessoa.objects.all()
    centrocustos = CentroCusto.objects.all()
    departamentos = Departamento.objects.all()
    
    listaProprietario = []
    listaBloco = []
    listaUnidade = []
    listaContato = []
    listaEmail = []

    for solicitacao in solicitacoes:
        solicitacao.data_ini = solicitacao.data_ini.strftime('%d/%m/%Y')

    for solicitacao in solicitacoesGeral:
        if solicitacao.proprietario_nome in listaProprietario:
            pass
        else:
            listaProprietario.append(solicitacao.proprietario_nome)
        if solicitacao.bloco in listaBloco:
            pass
        else:
            listaBloco.append(solicitacao.bloco)
        if solicitacao.unidade in listaUnidade:
            pass
        else:
            listaUnidade.append(solicitacao.unidade)
        if solicitacao.telefone1 in listaContato:
            pass
        else:
            listaContato.append(solicitacao.telefone1)
        if solicitacao.proprietario_email in listaEmail:
            pass
        else:
            listaEmail.append(solicitacao.proprietario_email)


    listaProprietario = sorted(listaProprietario)
    listaBloco = sorted(listaBloco)
    listaUnidade = sorted(listaUnidade)
    listaEmail = sorted(listaEmail)

    context = {
        'solicitacoes' : solicitacoes,
        'pessoas' : pessoas,
        'departamentos' : departamentos,
        'centrocustos' : centrocustos,
        'filtros' : filtrosWhere['filtros'],
        'usuario' : usuario,
        'listaProprietario' : listaProprietario,
        'listaBloco' : listaBloco,
        'listaUnidade' : listaUnidade,
        'listaContato' : listaContato,
        'listaEmail' : listaEmail,
        'status' : filtrosWhere['status'],
    }
    return render(request, 'listarSolicitacoes.html', context)

@login_required(login_url='/account/login')
def solicitacaoCliente(request):
    form = SolicitacaoForms()
    context = {
        "form" : form
    }
    return render(request, 'solicitacaoCliente.html', context)

@login_required(login_url='/account/login')
def dashboardsSat(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)
    centrocustos = CentroCusto.objects.all()

    listaMeses = []
    meses = []
    solicitacoes = DashboardSAT.objects.extra(where=[filtrosWhere['WHERE']]).order_by('data_ini')

    if (request.GET):
        dt_inicio = [request.GET['start'][0] + request.GET['start'][1], request.GET['start'][3] + request.GET['start'][4], request.GET['start'][6] + request.GET['start'][7] + request.GET['start'][8] + request.GET['start'][9]]
        dt_fim = [request.GET['end'][0] + request.GET['end'][1], request.GET['end'][3] + request.GET['end'][4], request.GET['end'][6] + request.GET['end'][7] + request.GET['end'][8] + request.GET['end'][9]]
        dataInicio = date(day=int(dt_inicio[0]), month=int(dt_inicio[1]), year=int(dt_inicio[2]))
        dataFim = date(day=int(dt_fim[0]), month=int(dt_fim[1]), year=int(dt_fim[2]))
        mesAtual = int(dt_inicio[1])
        anoAtual = dt_inicio[2]
    else:
        teste = str(solicitacoes[0].data_ini).split('-')
        dt_inicio = date(int(teste[0]),int(teste[1]),int(teste[2]))
        dt_fim = date.today()
        dataInicio = date(day=dt_inicio.day, month=dt_inicio.month, year=dt_inicio.year)
        dataFim = date(day=dt_fim.day, month=dt_fim.month, year=dt_fim.year)
        mesAtual = int(dt_inicio.month)
        anoAtual = int(dt_inicio.year)

    diferenca = (dataFim - dataInicio)
    meses_contador = int(diferenca.days) // 28
    if meses_contador == 0:
        meses_contador = 1
   
    for mes in range(0, int(meses_contador) + 1):
        if(mesAtual == 1):
            inicio = "Janeiro/" + str(anoAtual)
            mesAtual += 1
        elif(mesAtual == 2):
            inicio = "Fevereiro/" + str(anoAtual)
            mesAtual += 1
        elif(mesAtual == 3):
            inicio = "Março/" + str(anoAtual)
            mesAtual += 1
        elif(mesAtual == 4):
            inicio = "Abril/" + str(anoAtual)
            mesAtual += 1
        elif(mesAtual == 5):
            inicio = "Maio/" + str(anoAtual)
            mesAtual += 1
        elif(mesAtual == 6):
            inicio = "Junho/" + str(anoAtual)
            mesAtual += 1
        elif(mesAtual == 7):
            inicio = "Julho/" + str(anoAtual)
            mesAtual += 1
        elif(mesAtual == 8):
            inicio = "Agosto/" + str(anoAtual)
            mesAtual += 1
        elif(mesAtual == 9):
            inicio = "Setembro/" + str(anoAtual)
            mesAtual += 1
        elif(mesAtual == 10):
            inicio = "Outubro/" + str(anoAtual)
            mesAtual += 1
        elif(mesAtual == 11):
            inicio = "Novembro/" + str(anoAtual)
            mesAtual += 1
        elif(mesAtual == 12):
            inicio = "Dezembro/" + str(anoAtual)
            mesAtual = 1
            anoAtual = int(anoAtual) + int(1)
        meses.append(inicio)
        listaMeses.append(inicio)
        listaMeses.append(0)
        listaMeses.append(0)

    # Funcionamento das colunas
    sem_avaliacao = []
    ruim = []
    regular = []
    bom = []
    otimo = []
    
    fluxo = []
    reparo = []

    axf = []
    avaliacao = []
    solicitacao = []
      
    # for que puxa os dados do banco p/ graficos
    for solicitacao in solicitacoes:
        if solicitacao.empreendimento not in avaliacao:
            # Reparo
            tipo = [solicitacao.empreendimento,0,0,0,0,0,0,0,0,0,0]
            reparo.extend(tipo)
            # Satisfação
            tipo = [solicitacao.empreendimento,0,0,0,0,0]
            avaliacao.extend(tipo) 

        # Por Tipo de Reparo
        if solicitacao.tipo_reparo == "Especialista":
            reparo[reparo.index(solicitacao.empreendimento) + 1] += 1    

        if solicitacao.tipo_reparo == "Esquadrias de Alumínio":
            reparo[reparo.index(solicitacao.empreendimento) + 2] += 1    
        
        if solicitacao.tipo_reparo == "Esquadrias de Madeira":
            reparo[reparo.index(solicitacao.empreendimento) + 3] += 1    

        if solicitacao.tipo_reparo == "Instalações Elétricas":
            reparo[reparo.index(solicitacao.empreendimento) + 4] += 1    

        if solicitacao.tipo_reparo == "Instalações Hidráulicas":
            reparo[reparo.index(solicitacao.empreendimento) + 5] += 1    

        if solicitacao.tipo_reparo == "Instalações Gás":
            reparo[reparo.index(solicitacao.empreendimento) + 6] += 1    

        if solicitacao.tipo_reparo == "Limpeza":
            reparo[reparo.index(solicitacao.empreendimento) + 7] += 1

        if solicitacao.tipo_reparo == "Lógica e Telefone":
            reparo[reparo.index(solicitacao.empreendimento) + 8] += 1 

        if solicitacao.tipo_reparo == "Pintura":
            reparo[reparo.index(solicitacao.empreendimento) + 9] += 1 

        if solicitacao.tipo_reparo == "Serviço Civil":
            reparo[reparo.index(solicitacao.empreendimento) + 10] += 1 
        
        # Por Satisfação
        if solicitacao not in fluxo:
            if solicitacao.satisfacao_avaliacao == 1:
                avaliacao[avaliacao.index(solicitacao.empreendimento) + 1] += 1 
                
            elif solicitacao.satisfacao_avaliacao == 2:
                avaliacao[avaliacao.index(solicitacao.empreendimento) + 2] += 1

            elif solicitacao.satisfacao_avaliacao == 3:
                avaliacao[avaliacao.index(solicitacao.empreendimento) + 3] += 1

            elif solicitacao.satisfacao_avaliacao == 4:
                avaliacao[avaliacao.index(solicitacao.empreendimento) + 4] += 1
                
            elif solicitacao.satisfacao_avaliacao == 5:
                avaliacao[avaliacao.index(solicitacao.empreendimento) + 5] += 1
            fluxo.append(solicitacao)

            mesInicio = solicitacao.data_ini.month
            mesFim = solicitacao.data_fim.month
            ano = solicitacao.data_ini.year

            if(mesInicio == 1):
                inicio = "Janeiro/" + str(ano)
            elif(mesInicio == 2):
                inicio = "Fevereiro/" + str(ano)
            elif(mesInicio == 3):
                inicio = "Março/" + str(ano)
            elif(mesInicio == 4):
                inicio = "Abril/" + str(ano)
            elif(mesInicio == 5):
                inicio = "Maio/" + str(ano)
            elif(mesInicio == 6):
                inicio = "Junho/" + str(ano)
            elif(mesInicio == 7):
                inicio = "Julho/" + str(ano)
            elif(mesInicio == 8):
                inicio = "Agosto/" + str(ano)
            elif(mesInicio == 9):
                inicio = "Setembro/" + str(ano)
            elif(mesInicio == 10):
                inicio = "Outubro/" + str(ano)
            elif(mesInicio == 11):
                inicio = "Novembro/" + str(ano)
            elif(mesInicio == 12):
                inicio = "Dezembro/" + str(ano)

            if(mesFim == 1):
                fim = "Janeiro/" + str(ano)
            elif(mesFim == 2):
                fim = "Fevereiro/" + str(ano)
            elif(mesFim == 3):
                fim = "Março/" + str(ano)
            elif(mesFim == 4):
                fim = "Abril/" + str(ano)
            elif(mesFim == 5):
                fim = "Maio/" + str(ano)
            elif(mesFim == 6):
                fim = "Junho/" + str(ano)
            elif(mesFim == 7):
                fim = "Julho/" + str(ano)
            elif(mesFim == 8):
                fim = "Agosto/" + str(ano)
            elif(mesFim == 9):
                fim = "Setembro/" + str(ano)
            elif(mesFim == 10):
                fim = "Outubro/" + str(ano)
            elif(mesFim == 11):
                fim = "Novembro/" + str(ano)
            elif(mesFim == 12):
                fim = "Dezembro/" + str(ano)

            solicitacao.data_ini = solicitacao.data_ini.strftime('%d/%m/%Y')
            solicitacao.data_fim = solicitacao.data_fim.strftime('%d/%m/%Y')

            variavel = inicio
            variavelDois = fim
            try:
                listaMeses[listaMeses.index(variavel) + 1] += 1

                if solicitacao.stat == 'Feito':
                    listaMeses[listaMeses.index(variavelDois) + 2] += 1
            except:
                print("O mês: {mes} não está na lista".format(mes=variavelDois))

            # if variavel in meses: 
            #     listaMeses[listaMeses.index(variavel) + 1] += 1
            #     if solicitacao.stat == 'Feito':
            #         if variavelDois in meses:
            #             listaMeses[listaMeses.index(variavelDois) + 2] += 1
            #         else:
            #             # meses.append(variavelDois)
            #             # lista = [variavelDois,0,1]
            #             # listaMeses.extend(lista)
            #             aux = variavelDois, 0, 1
            #             if aux not in mesesFinalizados:
            #                 mesesFinalizados.append(aux)
                        
            # else:
            #     meses.append(variavel)
            #     if solicitacao.stat == 'Feito':
            #         if variavel == variavelDois:
            #             lista = [variavel,1,1]
            #         else:
            #             # meses.append(variavelDois)
            #             # lista = [variavel,1,0,variavelDois,0,1]
            #             aux = variavelDois, 0, 1
            #             if aux not in mesesFinalizados:
            #                 aux = variavelDois, 0, 1
            #                 mesesFinalizados.append(aux)
            #             # else:
            #             #     mesesFinalizados[mesesFinalizados.index(variavelDois) + 2] += 1
            #             lista = [variavel,1,0]
            #     else:
            #         lista = [variavel,1,0]
            #     listaMeses.extend(lista)

            # print("ID: {id}\nStatus: {status}\nInício: {inicio}\nFim: {fim}\nMeses: {meses}\nFinalizados: {finalizados}\n".format(id=solicitacao.id_tarefa, status=solicitacao.stat,  inicio=variavel, fim=variavelDois, meses=meses, finalizados=mesesFinalizados))

    print(listaMeses)
    qtdProcessos = [len(sem_avaliacao), len(ruim), len(regular), len(bom), len(otimo)]
    
    context = {
        'solicitacoes' : solicitacoes,
        'usuario' : usuario,
        'fluxo' : fluxo,
        
        'qtdProcessos' : qtdProcessos,

        'filtros' : filtrosWhere['filtros'],
        'centrocustos' : centrocustos,

        'avaliacao' : avaliacao,
        'reparo' : reparo,
        'axf' : axf,

        'meses' : meses,
        'listaMeses' : listaMeses
    }
    return render(request, 'dashboardsSat.html', context)

@login_required(login_url='/account/login')
def impressao(request, id):
    usuario = get_user(request.user)
    pessoas = Pessoa.objects.all()


    tarefa = get_object_or_404(Tarefa, id_tarefa=id)
    solicitacao = get_object_or_404(Solicitacao, id_tarefa=id)
    problema = Problema.objects.filter(id_solicitacao=solicitacao.id_solicitacao)
    executores = get_object_or_404(Executor, id_tarefa=id)
    form_executores = ExecutorForms(instance=executores)


    context = {
        'usuario' : usuario,
        "tarefa" : tarefa,
        'pessoas' : pessoas,
        'executores' : executores,
        'executores' : executores,
        "solicitacao" : solicitacao,
        "problema" : problema,
        "form_executores" : form_executores,
        "id" : id,
    }
    return render(request, 'impressao.html', context)

def getProblemas(request, id):
    if request.method == 'GET' and request.is_ajax():
        try:
            solicitacao = Solicitacao.objects.get(id_tarefa=id)
            problemas = Problema.objects.filter(id_solicitacao=solicitacao.id_solicitacao)
        except:
            problemas = ""

    data = serializers.serialize('json', list(problemas))
    return HttpResponse(json.dumps(data))

def exportarSolicitacoes(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    data = datetime.now().strftime('%Y-%m-%d')

    model = 'ExportarTarefa'

    filename = f'MyScrum Solicitações - SAT {data} ({usuario.nome}).xls'
    
    queryset = ExportarSolicitacoes.objects.all().extra(where=[filtrosWhere['WHERE']]).order_by('prioridade').values_list(
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
        'data_fim',
        'data_finalizacao',
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
        'processo_relacionado',
        'checado',
        'empreendimento',
        'bloco',
        'unidade',
        'proprietario_nome',
        'proprietario_rg',
        'proprietario_cpf',
        'proprietario_email',
        'solicitante_nome',
        'solicitante_rg',
        'solicitante_cpf',
        'solicitante_email',
        'telefone1',
        'telefone2',
        'status_processo',
        'status_solicitacao',
        'data_entrega',
        'tipo_solicitacao',
        'tempo_total',
        'satisfacao_avaliacao',
        'satisfacao_observacoes',
        'finalizado',
        'ambiente',
        'descricao_sat',
        'tipo_reparo',
        'procedencia',
        'historico_sat',
        'estimativa_custo',
        'duracao',
        'material',
        # 'data_inicial_p',
        # 'data_final_p',
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
        'data inicio',
        'data real',
        'data fim real',
        'data fim',
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
        'processo relacionado',
        'checado',
        'empreendimento',
        'bloco',
        'unidade',
        'proprietario nome',
        'proprietario rg',
        'proprietario cpf',
        'proprietario email',
        'solicitante nome',
        'solicitante rg',
        'solicitante cpf',
        'solicitante email',
        'telefone1',
        'telefone2',
        'status processo',
        'status solicitacao',
        'data_entrega',
        'tipo solicitacao',
        'tempo total',
        'satisfacao avaliacao',
        'satisfacao observacoes',
        'finalizado1',
        'ambiente1',
        'descricao sat1',
        'tipo reparo1',
        'procedencia1',
        'historico sat1',
        'estimativa custo1',
        'duracao1',
        'material1',
        # 'data inicial 1',
        # 'data final 1',
        'finalizado2',
        'ambiente2',
        'descricao sat2',
        'tipo reparo2',
        'procedencia2',
        'historico sat2',
        'estimativa custo2',
        'duracao2',
        'material2',
        # 'data inicial 2',
        # 'data final 2',
        'finalizado3',
        'ambiente3',
        'descricao sat3',
        'tipo reparo3',
        'procedencia3',
        'historico sat3',
        'estimativa custo3',
        'duracao3',
        'material3',
        # 'data inicial 3',
        # 'data final 3',
        'finalizado4',
        'ambiente4',
        'descricao sat4',
        'tipo reparo4',
        'procedencia4',
        'historico sat4',
        'estimativa custo4',
        'duracao4',
        'material4',
        # 'data inicial 4',
        # 'data final 4',
        'finalizado5',
        'ambiente5',
        'descricao sat5',
        'tipo reparo5',
        'procedencia5',
        'historico sat5',
        'estimativa custo5',
        'duracao5',
        'material5',
        # 'data inicial 5',
        # 'data final 5',
        'finalizado6',
        'ambiente6',
        'descricao sat6',
        'tipo reparo6',
        'procedencia6',
        'historico sat6',
        'estimativa custo6',
        'duracao6',
        'material6',
        # 'data inicial 6',
        # 'data final 6',
        'finalizado7',
        'ambiente7',
        'descricao sat7',
        'tipo reparo7',
        'procedencia7',
        'historico sat7',
        'estimativa custo7',
        'duracao7',
        'material7',
        # 'data inicial 7',
        # 'data final 7',
        'finalizado8',
        'ambiente8',
        'descricao sat8',
        'tipo reparo8',
        'procedencia8',
        'historico sat8',
        'estimativa custo8',
        'duracao8',
        'material8',
        # 'data inicial 8',
        # 'data final 8',
        'finalizado9',
        'ambiente9',
        'descricao sat9',
        'tipo reparo9',
        'procedencia9',
        'historico sat9',
        'estimativa custo9',
        'duracao9',
        'material9',
        # 'data inicial 9',
        # 'data final 9',
        'finalizado10',
        'ambiente10',
        'descricao sat10',
        'tipo reparo10',
        'procedencia10',
        'historico sat10',
        'estimativa custo10',
        'duracao10',
        'material10',
        # 'data inicial 10',
        # 'data final 10',
        'finalizado11',
        'ambiente11',
        'descricao sat11',
        'tipo reparo11',
        'procedencia11',
        'historico sat11',
        'estimativa custo11',
        'duracao11',
        'material11',
        # 'data inicial 11',
        # 'data final 11',
        'finalizado12',
        'ambiente12',
        'descricao sat12',
        'tipo reparo12',
        'procedencia12',
        'historico sat12',
        'estimativa custo12',
        'duracao12',
        'material12',
        # 'data inicial 12',
        # 'data final 12',
        'finalizado13',
        'ambiente13',
        'descricao sat13',
        'tipo reparo13',
        'procedencia13',
        'historico sat13',
        'estimativa custo13',
        'duracao13',
        'material13',
        # 'data inicial 13',
        # 'data final 13',
        'finalizado14',
        'ambiente14',
        'descricao sat14',
        'tipo reparo14',
        'procedencia14',
        'historico sat14',
        'estimativa custo14',
        'duracao14',
        'material14',
        # 'data inicial 14',
        # 'data final 14',
        'finalizado15',
        'ambiente15',
        'descricao sat15',
        'tipo reparo15',
        'procedencia15',
        'historico sat15',
        'estimativa custo15',
        'duracao15',
        'material15',
        # 'data inicial 15',
        # 'data final 15',
        'finalizado16',
        'ambiente16',
        'descricao sat16',
        'tipo reparo16',
        'procedencia16',
        'historico sat16',
        'estimativa custo16',
        'duracao16',
        'material16',
        # 'data inicial 16',
        # 'data final 16',
        'finalizado17',
        'ambiente17',
        'descricao sat17',
        'tipo reparo17',
        'procedencia17',
        'historico sat17',
        'estimativa custo17',
        'duracao17',
        'material17',
        # 'data inicial 17',
        # 'data final 17',
        'finalizado18',
        'ambiente18',
        'descricao sat18',
        'tipo reparo18',
        'procedencia18',
        'historico sat18',
        'estimativa custo18',
        'duracao18',
        'material18',
        # 'data inicial 18',
        # 'data final 18',
        'finalizado19',
        'ambiente19',
        'descricao sat19',
        'tipo reparo19',
        'procedencia19',
        'historico sat19',
        'estimativa custo19',
        'duracao19',
        'material19',
        # 'data inicial 19',
        # 'data final 19',
        'finalizado20',
        'ambiente20',
        'descricao sat20',
        'tipo reparo20',
        'procedencia20',
        'historico sat20',
        'estimativa custo20',
        'duracao20',
        'material20',
        # 'data inicial 20',
        # 'data final 20',
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
    
    listaSolicitacoes = []
    i = 0
    for solicitacao in queryset:
        if solicitacao[38] == "Solicitação Assistência Técnica":
            if len(listaSolicitacoes) > 0:
                for a in range(len(listaSolicitacoes)):
                    if solicitacao[0] in listaSolicitacoes[a]:
                        cList = list(listaSolicitacoes[a])
                        if solicitacao[60] == None:
                            status_finalizado = "Não"
                        else:
                            if solicitacao[60] == 1:
                                status_finalizado = "Sim"  
                            else:
                                status_finalizado = "Não"
                        problemas = [status_finalizado, solicitacao[61], solicitacao[62], solicitacao[63], solicitacao[64], solicitacao[65], solicitacao[66], solicitacao[67], solicitacao[68]]
                        if solicitacao[0] == 85128:
                            print(solicitacao[0], problemas)
                        cList.extend(problemas)
                        listaSolicitacoes[a] = cList
                        break                   
                else:
                    cList = list(solicitacao)
                    if cList[60] == 1:
                        cList[60] = "Sim"  
                    else:
                        cList[60] = "Não"
                    listaSolicitacoes.append(cList)
            else:
                cList = list(solicitacao)
                if cList[60] == 1:
                    cList[60] = "Sim"  
                else:
                    cList[60] = "Não"
                listaSolicitacoes.append(cList)

    rows = listaSolicitacoes

    for row, rowdata in enumerate(rows):
        row_num += 1
        for col, val in enumerate(rowdata):
            ws.write(row_num, col, val, default_style)
    wb.save(response)
    return response

# Função que gera os filtros baseado no form do request 
def gerarFiltros(request, usuario):
    solicitacoes = []
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
        data_inicio = date(2000, 1, 1 )

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
    ################# Filtro de Bloco ############################\
    #################-------------------##########################

    #################-------------------############################
    ################# Filtro de Unidade ############################
    unidades = request.GET.getlist('unidade')
    if len(unidades):
        filtros['unidade'] = unidades
        unidades = str(unidades).replace('[','(').replace(']',')')
        filtrosUnidades = f''' unidade in {unidades} AND '''
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

    CASE 
        WHEN id_empresa = {usuario.id_empresa} and stat = 'A fazer' or stat = 'Fazendo' or stat = 'Feito' or stat = 'Cancelado'
            THEN 
                data_ini BETWEEN '{data_inicio}' AND '{data_fim}' 
    END
    """
    # WHEN id_empresa = {usuario.id_empresa} and stat = 'A fazer' or id_empresa = {usuario.id_empresa} and stat = 'Fazendo' or id_empresa = {usuario.id_empresa} and stat = 'Feito' or id_empresa = {usuario.id_empresa} and stat = 'Cancelado'
    retorno = {
        'filtros' : filtros,
        'WHERE' : WHERE,
        'status' : status
    }

    return retorno
