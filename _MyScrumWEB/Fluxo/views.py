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
from Solicitacao.models import Problema
from Solicitacao.views import ExportarSolicitacoes

# Import de mesmo App
from .models import FluxoSAT, FluxoLocacao, FluxoMedicaoTerceiros, ExportarLocacao, LocacaoEditar, ExportarMedicao, Juridico, FluxoJuridico, Testemunhas, Autor, Reu, LocacaoConservacao
from .forms import EditarLocacao

# Import Biblioteca Python
from datetime import date, datetime, timedelta
import json
import xlrd
import xlwt
import os

# Create your views here.

def fluxo(request):
    return render(request, 'fluxo.html')

@login_required(login_url=urls.getUrlSubdominio())
def solicitacao(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    solicitacoes = FluxoSAT.objects.extra(where=[filtrosWhere['WHERE']]).order_by('prioridade')
    solicitacoesGeral = FluxoSAT.objects.all()

    pessoas = Pessoa.objects.all()
    centrocustos = CentroCusto.objects.all()
    departamentos = Departamento.objects.all()
    
    # Funcionamento dos filtros
    listaProprietario = []
    listaBloco = []
    listaUnidade = []
    listaContato = []
    listaEmail = []

    # Funcionamento das colunas
    analise = []
    agendamento = []
    atendimento = []
    termoQuitacao = []
    juridico = []
    concluido = []
    foraGarantia = []

    fluxo = []
    problemasAnalise = []
    finalizadosAnalise = []
    problemasAgendamento = []
    finalizadosAgendamento = []
    problemasAtendimento = []
    finalizadosAtendimento = []
    problemasTermo = []
    finalizadosTermo = []
    problemasJuridico = []
    finalizadosJuridico = []
    problemasConcluido = []
    finalizadosConcluido = []
    problemasGarantia = []
    finalizadosGarantia = []

    for solicitacao in solicitacoes:
        if solicitacao not in fluxo:
            solicitacao.data_ini = solicitacao.data_ini.strftime('%d/%m/%Y')
            solicitacao.data_fim = solicitacao.data_fim.strftime('%d/%m/%Y')
            solicitacao.data_entrega = solicitacao.data_entrega.strftime('%d/%m/%Y')
            problemas = Problema.objects.filter(id_solicitacao=solicitacao.id_solicitacao)
            qtdProblemas = 0
            qtdFinalizados = 0
            for problema in problemas:
                qtdProblemas += 1
                if problema.finalizado != None and problema.finalizado != 0:
                    qtdFinalizados += 1
            if solicitacao.status_processo == "Análise" and solicitacao.processo_relacionado == 'Solicitação Assistência Técnica':
                analise.append(solicitacao)
                problemasAnalise.append(qtdProblemas)
                finalizadosAnalise.append(qtdFinalizados)
            elif solicitacao.status_processo == "Agendamento" and solicitacao.processo_relacionado == 'Solicitação Assistência Técnica':
                agendamento.append(solicitacao)
                problemasAgendamento.append(qtdProblemas)
                finalizadosAgendamento.append(qtdFinalizados)
            elif solicitacao.status_processo == "Atendimento" and solicitacao.processo_relacionado == 'Solicitação Assistência Técnica':
                atendimento.append(solicitacao)
                problemasAtendimento.append(qtdProblemas)
                finalizadosAtendimento.append(qtdFinalizados)
            elif solicitacao.status_processo == "Termo de Quitação" and solicitacao.processo_relacionado == 'Solicitação Assistência Técnica':
                termoQuitacao.append(solicitacao)
                problemasTermo.append(qtdProblemas)
                finalizadosTermo.append(qtdFinalizados)
            elif solicitacao.status_processo == "Jurídico" and solicitacao.processo_relacionado == 'Solicitação Assistência Técnica':
                juridico.append(solicitacao)
                problemasJuridico.append(qtdProblemas)
                finalizadosJuridico.append(qtdFinalizados)
            elif solicitacao.status_processo == "Concluído" and solicitacao.processo_relacionado == 'Solicitação Assistência Técnica':
                concluido.append(solicitacao)
                problemasConcluido.append(qtdProblemas)
                finalizadosConcluido.append(qtdFinalizados)
            elif solicitacao.status_processo == "Fora de Garantia" and solicitacao.processo_relacionado == 'Solicitação Assistência Técnica':
                foraGarantia.append(solicitacao)
                problemasGarantia.append(qtdProblemas)
                finalizadosGarantia.append(qtdFinalizados)
            fluxo.append(solicitacao)
            
    qtdProcessos = [len(analise), len(agendamento), len(atendimento), len(termoQuitacao), len(juridico), len(concluido), len(foraGarantia)]
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
        'usuario' : usuario,
        'pessoas' : pessoas,
        'departamentos' : departamentos,
        'centrocustos' : centrocustos,
        'fluxo' : fluxo,

        'listaProprietario' : listaProprietario,
        'listaBloco' : listaBloco,
        'listaUnidade' : listaUnidade,
        'listaContato' : listaContato,
        'listaEmail' : listaEmail,

        'analise' : analise,
        'agendamento' : agendamento,
        'atendimento' : atendimento,
        'termoQuitacao' : termoQuitacao,
        'juridico' : juridico,
        'concluido' : concluido,
        'foraGarantia' : foraGarantia,
        
        'qtdProcessos' : qtdProcessos,

        'problemasAnalise' : problemasAnalise,
        'finalizadosAnalise' : finalizadosAnalise,
        'problemasAgendamento' : problemasAgendamento,
        'finalizadosAgendamento' : finalizadosAgendamento,
        'problemasAtendimento' : problemasAtendimento,
        'finalizadosAtendimento' : finalizadosAtendimento,
        'problemasTermo' : problemasTermo,
        'finalizadosTermo' : finalizadosTermo,
        'problemasJuridico' : problemasJuridico,
        'finalizadosJuridico' : finalizadosJuridico,
        'problemasConcluido' : problemasConcluido,
        'finalizadosConcluido' : finalizadosConcluido,
        'problemasGarantia' : problemasGarantia,
        'finalizadosGarantia' : finalizadosGarantia,

        'filtros' : filtrosWhere['filtros'],
        'status' : filtrosWhere['status'],
    }
    return render(request, 'solicitacao.html', context)

@login_required(login_url=urls.getUrlSubdominio())
def conservacao(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    solicitacoes = FluxoSAT.objects.extra(where=[filtrosWhere['WHERE']]).order_by('prioridade')
    solicitacoesGeral = FluxoSAT.objects.all()
    locacoesLimpeza = FluxoLocacao.objects.filter(id_status = 7)
    fazerLimpeza = locacoesLimpeza.filter(stat='A fazer')
    fazendoLimpeza = locacoesLimpeza.filter(stat='Fazendo')

    pessoas = Pessoa.objects.all()
    centrocustos = CentroCusto.objects.all()
    departamentos = Departamento.objects.all()
    
    # Funcionamento dos filtros
    listaProprietario = []
    listaBloco = []
    listaUnidade = []
    listaContato = []
    listaEmail = []

    # Funcionamento das colunas
    agendamento = []
    limpeza = []
    limpezaLocacao = []
    manutencao = []
    pagar = []
    concluido = []

    fluxo = []
    problemasAgendamento = []
    finalizadosAgendamento = []
    problemasLimpeza = []
    finalizadosLimpeza = []
    problemasManutencao = []
    finalizadosManutencao = []
    problemasPagar = []
    finalizadosPagar = []
    problemasConcluido = []
    finalizadosConcluido = []

    for solicitacao in solicitacoes:
        if solicitacao not in fluxo:
            solicitacao.data_ini = solicitacao.data_ini.strftime('%d/%m/%Y')
            solicitacao.data_fim = solicitacao.data_fim.strftime('%d/%m/%Y')
            solicitacao.data_entrega = solicitacao.data_entrega.strftime('%d/%m/%Y')
            problemas = Problema.objects.filter(id_solicitacao=solicitacao.id_solicitacao)
            qtdProblemas = 0
            qtdFinalizados = 0
            for problema in problemas:
                if problema.ambiente != None:
                    qtdProblemas += 1
                    if problema.finalizado != None and problema.finalizado != 0:
                        qtdFinalizados += 1
            if solicitacao.status_processo == "Limpeza" and solicitacao.processo_relacionado == 'Conservação / Limpeza':
                limpeza.append(solicitacao)
                problemasLimpeza.append(qtdProblemas)
                finalizadosLimpeza.append(qtdFinalizados)
            elif solicitacao.status_processo == "Agendamento" and solicitacao.processo_relacionado == 'Conservação / Limpeza':
                agendamento.append(solicitacao)
                problemasAgendamento.append(qtdProblemas)
                finalizadosAgendamento.append(qtdFinalizados)
            elif solicitacao.status_processo == "Manutenção" and solicitacao.processo_relacionado == 'Conservação / Limpeza':
                if solicitacao.id_status != 10:
                    manutencao.append(solicitacao)
                    problemasManutencao.append(qtdProblemas)
                    finalizadosManutencao.append(qtdFinalizados)
            elif solicitacao.status_processo == "Pagar" and solicitacao.processo_relacionado == 'Conservação / Limpeza':
                pagar.append(solicitacao)
                problemasPagar.append(qtdProblemas)
                finalizadosPagar.append(qtdFinalizados)
            elif solicitacao.status_processo == "Concluído" and solicitacao.processo_relacionado == 'Conservação / Limpeza':
                concluido.append(solicitacao)
                problemasConcluido.append(qtdProblemas)
                finalizadosConcluido.append(qtdFinalizados)
            fluxo.append(solicitacao)
    
    for solicitacao in fazerLimpeza:
        limpezaLocacao.append(solicitacao)

    for solicitacao in fazendoLimpeza:
        limpezaLocacao.append(solicitacao)

    qtdProcessos = [len(limpeza), len(agendamento), len(manutencao), len(pagar), len(concluido), len(limpezaLocacao)]
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
        'usuario' : usuario,
        'pessoas' : pessoas,
        'departamentos' : departamentos,
        'centrocustos' : centrocustos,
        'fluxo' : fluxo,

        'listaProprietario' : listaProprietario,
        'listaBloco' : listaBloco,
        'listaUnidade' : listaUnidade,
        'listaContato' : listaContato,
        'listaEmail' : listaEmail,

        'limpeza' : limpeza,
        'limpezaLocacao' : limpezaLocacao,
        'agendamento' : agendamento,
        'manutencao' : manutencao,
        'pagar' : pagar,
        'concluido' : concluido,
        
        'qtdProcessos' : qtdProcessos,

        'problemasLimpeza' : problemasLimpeza,
        'finalizadosLimpeza' : finalizadosLimpeza,
        'problemasAgendamento' : problemasAgendamento,
        'finalizadosAgendamento' : finalizadosAgendamento,
        'problemasManutencao' : problemasManutencao,
        'finalizadosManutencao' : finalizadosManutencao,
        'problemasPagar' : problemasPagar,
        'finalizadosPagar' : finalizadosPagar,
        'problemasConcluido' : problemasConcluido,
        'finalizadosConcluido' : finalizadosConcluido,

        'filtros' : filtrosWhere['filtros'],
        'status' : filtrosWhere['status'],
    }
    return render(request, 'conservacao.html', context)

@login_required(login_url=urls.getUrlSubdominio())
def locacao(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltrosLocacao(request, usuario)

    locacoes = FluxoLocacao.objects.extra(where=[filtrosWhere['WHERE']]).order_by('prioridade')
    locacoesGeral = FluxoLocacao.objects.all()
    conservacoes = LocacaoConservacao.objects.all()
    
    pessoas = Pessoa.objects.all()
    centrocustos = CentroCusto.objects.all()
    departamentos = Departamento.objects.all()

    mae = []
    manutencao = []
    # negociacao = []
    # contrato = []
    energia = []
    orcar = []
    pagar = []
    instalar = []
    limpar = []
    vistoria = []
    # chave = []
    retorno = []
    feito = []

    listaBloco = []
    listaUnidade = []

    for locacao in locacoes:
        filhas = FluxoLocacao.objects.filter(id_locacao=locacao.id_locacao)
        for filha in filhas:
            if filha.stat != "Cancelado":
                filha.data_ini = filha.data_ini.strftime('%d/%m/%Y')
                filha.data_fim = filha.data_fim.strftime('%d/%m/%Y')
                if filha.id_status == 0:
                    mae.append(filha)
                # elif filha.id_status == 1 and filha.stat != "Feito":
                #     negociacao.append(filha)
                # elif filha.id_status == 2 and filha.stat != "Feito":
                #     contrato.append(filha)
                elif filha.id_status == 3 and filha.stat != "Feito":
                    energia.append(filha)
                elif filha.id_status == 4 and filha.stat != "Feito":
                    orcar.append(filha)
                elif filha.id_status == 5 and filha.stat != "Feito":
                    pagar.append(filha)
                elif filha.id_status == 6 and filha.stat != "Feito":
                    instalar.append(filha)
                elif filha.id_status == 7 and filha.stat != "Feito":
                    limpar.append(filha)
                elif filha.id_status == 8 and filha.stat != "Feito":
                    vistoria.append(filha)
                # elif filha.id_status == 9 and filha.stat != "Feito":
                #     chave.append(filha)
                elif filha.id_status == 10 and filha.stat != "Feito":
                    manutencao.append(filha)
                elif filha.id_status == 11 and filha.stat != "Feito":
                    retorno.append(filha)
                elif filha.stat == "Feito":
                    feito.append(filha)
                else:
                    print(filha.id_status)

    for locacao in locacoesGeral:
        if locacao.lBloco in listaBloco:
            pass
        else:
            listaBloco.append(locacao.lBloco)
        if locacao.lUnidade in listaUnidade:
            pass
        else:
            listaUnidade.append(locacao.lUnidade)

    for conservacao in conservacoes:
        conservacao.data_ini = conservacao.data_ini.strftime('%d/%m/%Y')
        conservacao.data_fim = conservacao.data_fim.strftime('%d/%m/%Y')
        if conservacao.status_processo == 'Manutenção':
            manutencao.append(conservacao)
        elif conservacao.status_processo == 'Limpeza':
            limpar.append(conservacao)
        else:
            print("Conservação fora dos processos")

    listaBloco.sort()
    listaUnidade.sort()

    context = {
        'locacoes' : locacoes,
        'usuario' : usuario,
        'pessoas' : pessoas,
        'departamentos' : departamentos,
        'centrocustos' : centrocustos,

        'mae' : mae,
        'manutencao' : manutencao,
        # 'negociacao' : negociacao,
        # 'contrato' : contrato,
        'energia' : energia,
        'orcar' : orcar,
        'pagar' : pagar,
        'instalar' : instalar,
        'limpar' : limpar,
        'vistoria' : vistoria,
        # 'chave' : chave,
        'retorno' : retorno,
        'feito' : feito,

        'listaBloco' : listaBloco,
        'listaUnidade' : listaUnidade,

        'filtros' : filtrosWhere['filtros'],
        'status' : filtrosWhere['status'],
    }
    return render(request, 'locacao.html', context)

@login_required(login_url=urls.getUrlSubdominio())
def medicaoTerceiros(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    medicoes = FluxoMedicaoTerceiros.objects.extra(where=[filtrosWhere['WHERE']]).order_by('prioridade')

    pessoas = Pessoa.objects.all()
    centrocustos = CentroCusto.objects.all()
    departamentos = Departamento.objects.all()

    elaboracao = []
    validacao = []
    documentacao = []
    nf = []
    titulo = []
    feito = []

    for medicao in medicoes:
        if medicao.id_medicao != 0:
            medicao.data_ini = medicao.data_ini.strftime('%d/%m/%Y')
            medicao.data_fim = medicao.data_fim.strftime('%d/%m/%Y')
            if medicao.id_medicao == 1 and medicao.stat != "Feito":
                elaboracao.append(medicao)
            elif medicao.id_medicao == 2 and medicao.stat != "Feito":
                validacao.append(medicao)
            elif medicao.id_medicao == 3 and medicao.stat != "Feito":
                documentacao.append(medicao)
            elif medicao.id_medicao == 4 and medicao.stat != "Feito":
                nf.append(medicao)
            elif medicao.id_medicao == 5 and medicao.stat != "Feito":
                titulo.append(medicao)
            elif medicao.stat == "Feito":
                feito.append(medicao)
            else:
                print(medicao.id_medicao)

    context = {
        'medicoes' : medicoes,
        'usuario' : usuario,
        'pessoas' : pessoas,
        'departamentos' : departamentos,
        'centrocustos' : centrocustos,

        'elaboracao' : elaboracao,
        'validacao' : validacao,
        'documentacao' : documentacao,
        'nf' : nf,
        'titulo' : titulo,
        'feito' : feito,

        'filtros' : filtrosWhere['filtros'],
        'status' : filtrosWhere['status'],
    }
    return render(request, 'medicaoTerceiros.html', context)

@login_required(login_url=urls.getUrlSubdominio())
def juridico(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    juridicos = FluxoJuridico.objects.extra(where=[filtrosWhere['WHERE']])
    juridicosGeral = FluxoJuridico.objects.all()

    pessoas = Pessoa.objects.all()
    centrocustos = CentroCusto.objects.all()
    departamentos = Departamento.objects.all()

    mae = []
    principal = []
    defesa = []
    replica = []
    audiencia = []
    finais = []   
    sentenca = []
    recurso2 = []
    recurso3 = []
    feito = []

    for juridico in juridicos:
        if juridico.id_juridico != 0:
            juridico.data_ini = juridico.data_ini.strftime('%d/%m/%Y')
            juridico.data_fim = juridico.data_fim.strftime('%d/%m/%Y')
            if juridico.id_status == 1 and juridico.stat != "Feito":
                mae.append(juridico)
            elif juridico.id_status == 2 and juridico.stat != "Feito":
                principal.append(juridico)
            elif juridico.id_status == 3 and juridico.stat != "Feito":
                defesa.append(juridico)
            elif juridico.id_status == 4 and juridico.stat != "Feito":
                replica.append(juridico)
            elif juridico.id_status == 5 and juridico.stat != "Feito":
                audiencia.append(juridico)
            elif juridico.id_status == 6 and juridico.stat != "Feito":
                finais.append(juridico)
            elif juridico.id_status == 7 and juridico.stat != "Feito":
                sentenca.append(juridico)
            elif juridico.id_status == 8 and juridico.stat != "Feito":
                recurso2.append(juridico)
            elif juridico.id_status == 9 and juridico.stat != "Feito":
                recurso3.append(juridico)
            elif juridico.stat == "Feito":
                feito.append(juridico)
            else:
                print(juridico.id_juridico)

    listaBloco = []
    listaUnidade = []
    listaEscritorio = []
    listaProcesso = []
    listaAutor = []
    listaReu = []
    listaTestemunha = []

    for juridico in juridicosGeral:
        if juridico.id_status == 1:
            # Bloco
            if juridico.jBloco not in listaBloco and juridico.jBloco != None:
                listaBloco.append(juridico.jBloco)
            # Unidade
            if juridico.jUnidade not in listaUnidade and juridico.jUnidade != None:
                listaUnidade.append(juridico.jUnidade)
            # Autor
            try:
                autores = get_object_or_404(Autor, id_tarefa=juridico.id_juridico)
                if autores.autor1 not in listaAutor and autores.autor1 != None:
                    listaAutor.append(autores.autor1)
                if autores.autor2 not in listaAutor and autores.autor2 != None:
                    listaAutor.append(autores.autor2)
                if autores.autor3 not in listaAutor and autores.autor3 != None:
                    listaAutor.append(autores.autor3)
                if autores.autor4 not in listaAutor and autores.autor4 != None:
                    listaAutor.append(autores.autor4)
                if autores.autor5 not in listaAutor and autores.autor5 != None:
                    listaAutor.append(autores.autor5)
                if autores.autor6 not in listaAutor and autores.autor6 != None:
                    listaAutor.append(autores.autor6)
                if autores.autor7 not in listaAutor and autores.autor7 != None:
                    listaAutor.append(autores.autor7)
                if autores.autor8 not in listaAutor and autores.autor8 != None:
                    listaAutor.append(autores.autor8)
                if autores.autor9 not in listaAutor and autores.autor9 != None:
                    listaAutor.append(autores.autor9)
                if autores.autor10 not in listaAutor and autores.autor10 != None:
                    listaAutor.append(autores.autor10)
            except:
                pass
            # Réu
            try:
                reus = get_object_or_404(Reu, id_tarefa=juridico.id_juridico)
                if reus.reu1 not in listaReu and reus.reu1 != None:
                    listaReu.append(reus.reu1)
                if reus.reu2 not in listaReu and reus.reu2 != None:
                    listaReu.append(reus.reu2)
                if reus.reu3 not in listaReu and reus.reu3 != None:
                    listaReu.append(reus.reu3)
                if reus.reu4 not in listaReu and reus.reu4 != None:
                    listaReu.append(reus.reu4)
                if reus.reu5 not in listaReu and reus.reu5 != None:
                    listaReu.append(reus.reu5)
                if reus.reu6 not in listaReu and reus.reu6 != None:
                    listaReu.append(reus.reu6)
                if reus.reu7 not in listaReu and reus.reu7 != None:
                    listaReu.append(reus.reu7)
                if reus.reu8 not in listaReu and reus.reu8 != None:
                    listaReu.append(reus.reu8)
                if reus.reu9 not in listaReu and reus.reu9 != None:
                    listaReu.append(reus.reu9)
                if reus.reu10 not in listaReu and reus.reu10 != None:
                    listaReu.append(reus.reu10)
            except:
                pass
            # Testemunhas
            try:
                testemunhas = get_object_or_404(Testemunhas, id_tarefa=juridico.id_juridico)
                if testemunhas.testemunha1 not in listaTestemunha and testemunhas.testemunha1 != None:
                    listaTestemunha.append(testemunhas.testemunha1)
                if testemunhas.testemunha2 not in listaTestemunha and testemunhas.testemunha2 != None:
                    listaTestemunha.append(testemunhas.testemunha2)
                if testemunhas.testemunha3 not in listaTestemunha and testemunhas.testemunha3 != None:
                    listaTestemunha.append(testemunhas.testemunha3)
                if testemunhas.testemunha4 not in listaTestemunha and testemunhas.testemunha4 != None:
                    listaTestemunha.append(testemunhas.testemunha4)
                if testemunhas.testemunha5 not in listaTestemunha and testemunhas.testemunha5 != None:
                    listaTestemunha.append(testemunhas.testemunha5)
                if testemunhas.testemunha6 not in listaTestemunha and testemunhas.testemunha6 != None:
                    listaTestemunha.append(testemunhas.testemunha6)
                if testemunhas.testemunha7 not in listaTestemunha and testemunhas.testemunha7 != None:
                    listaTestemunha.append(testemunhas.testemunha7)
                if testemunhas.testemunha8 not in listaTestemunha and testemunhas.testemunha8 != None:
                    listaTestemunha.append(testemunhas.testemunha8)
                if testemunhas.testemunha9 not in listaTestemunha and testemunhas.testemunha9 != None:
                    listaTestemunha.append(testemunhas.testemunha9)
                if testemunhas.testemunha10 not in listaTestemunha and testemunhas.testemunha10 != None:
                    listaTestemunha.append(testemunhas.testemunha10)
            except:
                pass
            # Testemunhas
            if juridico.escritorio not in listaEscritorio and juridico.escritorio != None:
                listaEscritorio.append(juridico.escritorio)
            # Nº Processo
            if juridico.numero_processo not in listaProcesso and juridico.numero_processo != None:
                listaProcesso.append(juridico.numero_processo)

    context = {
        'juridicos' : juridicos,
        'usuario' : usuario,
        'pessoas' : pessoas,
        'departamentos' : departamentos,
        'centrocustos' : centrocustos,

        'mae' : mae,
        'principal' : principal,
        'defesa' : defesa,
        'replica' : replica,
        'audiencia' : audiencia,
        'finais' : finais,
        'sentenca' : sentenca,
        'recurso2' : recurso2,
        'recurso3' : recurso3,
        'feito' : feito,

        'listaBloco': listaBloco,
        'listaUnidade' : listaUnidade,
        'listaEscritorio': listaEscritorio,
        'listaProcesso' : listaProcesso,
        'listaAutor' : listaAutor,
        'listaReu' : listaReu,
        'listaTestemunha' : listaTestemunha,

        'filtros' : filtrosWhere['filtros'],
        'status' : filtrosWhere['status'],
    }
    return render(request, 'juridico.html', context)

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

def gerarFiltrosLocacao(request, usuario):
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
        status = "('A fazer', 'Fazendo')"

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
    blocos = request.GET.getlist('lBloco')
    if len(blocos):
        filtros['lBloco'] = blocos
        blocos = str(blocos).replace('[','(').replace(']',')')
        filtrosBlocos = f''' lBloco in {blocos} AND '''
    ################# Filtro de Bloco ############################
    #################-------------------##########################

    #################-------------------############################
    ################# Filtro de Unidade ############################
    unidades = request.GET.getlist('lUnidade')
    if len(unidades):
        filtros['lUnidade'] = unidades
        unidades = str(unidades).replace('[','(').replace(']',')')
        filtrosUnidades = f''' lUnidade in {unidades} AND '''
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

    CASE 
        WHEN id_status = 0 and stat = 'A fazer' and id_empresa = {usuario.id_empresa} or id_status = 0 and stat = 'Fazendo' and id_empresa = {usuario.id_empresa} or id_status = 0 and stat = 'Feito' and id_empresa = {usuario.id_empresa} or id_status = 11 and id_empresa = {usuario.id_empresa}
            THEN 
                stat != 'Cancelado'
    END
    """

    retorno = {
        'filtros' : filtros,
        'WHERE' : WHERE,
        'status' : status
    }

    return retorno

def exportarConservacao(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    data = datetime.now().strftime('%Y-%m-%d')

    model = 'ExportarTarefa'

    filename = f'MyScrum Solicitações - Conservação / Limpeza {data} ({usuario.nome}).xls'
    
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
        'data incio',
        'data fim',
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
        if solicitacao[38] == "Conservação / Limpeza":
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

def exportarLocacao(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    data = datetime.now().strftime('%Y-%m-%d')

    model = 'ExportarLocacao'

    filename = f'MyScrum - Locações {data} ({usuario.nome}).xls'
    
    queryset = ExportarLocacao.objects.all().extra(where=[filtrosWhere['WHERE']]).order_by('prioridade').values_list(
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
        'id_locacao',
        'id_status',
        'lBloco',
        'lUnidade',
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
        'id_locacao',
        'id_status',
        'Bloco',
        'Unidade',
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

def exportarMedicao(request):
    usuario = get_user(request.user)

    filtrosWhere = gerarFiltros(request, usuario)

    data = datetime.now().strftime('%Y-%m-%d')

    model = 'ExportarMedicao'

    filename = f'MyScrum - Medições {data} ({usuario.nome}).xls'
    
    queryset = ExportarMedicao.objects.all().extra(where=[filtrosWhere['WHERE']]).order_by('prioridade').values_list(
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
        'mes',
        'valor_bruto',
        'valor_liquido',
        'permuta',
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
        'mes',
        'valor bruto',
        'valor liquido',
        'permuta',
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

@login_required(login_url=urls.getUrlSubdominio())
def editarLocacao(request, id):
    usuario = get_user(request.user)
    locacao = get_object_or_404(LocacaoEditar, id_locacao_editar=id)
    form = EditarLocacao(instance=locacao)

    if request.method == 'POST':
        # Buscando a instancia da tarefa e criando o form carregando os dados do POST
        locacao = get_object_or_404(LocacaoEditar, pk=id)
        form = EditarLocacao(request.POST, instance=locacao)

        # Valida e salva
        if form.is_valid():
            locacao = form.save(commit=False)
            locacao.save()

            messages.success(request, 'A Locação foi atualizada com sucesso!', extra_tags='success')
            return HttpResponseRedirect(reverse('Fluxo:editarLocacao', args=(id,)))
        
        else:
            print(form.errors)

            messages.success(request, 'Falha ao atualizar a tarefa', extra_tags='danger')
            return HttpResponseRedirect(reverse('Fluxo:editarLocacao', args=(id,)))

    context = {
        'locacao' : locacao,
        'usuario' : usuario,
        'form' : form
    }
    return render(request, 'editarLocacao.html', context)
