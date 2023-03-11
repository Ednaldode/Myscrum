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
from .forms import EntregaForms
from .models import Entrega

# Import Biblioteca Python
from datetime import date, datetime, timedelta
from random import randint
import json
import threading
import time


# Create your views here.

#########################################################################################
# Copia do views de Cadastro de tarefas
#########################################################################################


@login_required(login_url=urls.getUrlSubdominio())
def entregachaves(request):
    descri_pesquisa = ""
    usuarios = request.GET.getlist('pessoa')
    usuario = "Varios Usuarios"
    form = EntregaForms()

    if len(usuarios) == 1:
        user = Pessoa.objects.get(nome=usuarios[0]).id_user
        usuario = get_user(user)
        usuarios.append('valor para não bugar a tupla')

    if len(usuarios) == 0:
        user = request.user
        usuario = get_user(user)
        usuarios.append(usuario.nome)
        usuarios.append('valor para não bugar a tupla')

    # try:
    #     tarefa = get_object_or_404(Entrega, pk=id)
    # except:
    #     tarefa = ""

    filtros = {}
    filtrosCC = ""

    #################--------------------##########################
    ################# Filtro de Centro de custo ##################
    # Se o campo centrocusto não estiver vazio filtra tarefas baseada no centrocusto de custo escolhido
    if request.GET.get('centrocusto') != None and request.GET.get('centrocusto') != 'Centros de custo':
        filtros['centrocusto'] = CentroCusto.objects.get(
            id_centro_custo=request.GET.get('centrocusto')).centrocusto
        centro_custo = CentroCusto.objects.get(
            id_centro_custo=request.GET.get('centrocusto')).centrocusto
        filtrosCC = f''' centro_custo = '{centro_custo}' AND '''
    ################# Filtro de Centro de custo ##################
    #################--------------------##########################

    WHERE = f"""
    {filtrosCC}

    """

    centrocustos = CentroCusto.objects.all().exclude(id_sienge=None)
    
    if request.method == 'POST':
        form = EntregaForms(request.POST)
        if form.is_valid():
            formulario = Entrega(
                empreendimento = form.cleaned_data['empreendimento'],
                bloco = form.cleaned_data['bloco'],
                apto = form.cleaned_data['apto'],
                data_entrega = form.cleaned_data['data_entrega'],
                data_assin = form.cleaned_data['data_assin'],
                proprietario1 = form.cleaned_data['proprietario1'],
                proprietario2 = form.cleaned_data['proprietario2'],
                testemunha1 = form.cleaned_data['testemunha1'],
                testemunha2 = form.cleaned_data['testemunha2'],
                rg_proprietario1 = form.cleaned_data['rg_proprietario1'],
                rg_proprietario2 = form.cleaned_data['rg_proprietario2'],
                rg_testemunha1 = form.cleaned_data['rg_testemunha1'],
                rg_testemunha2 = form.cleaned_data['rg_testemunha2'],
                cpf_proprietario1 = form.cleaned_data['cpf_proprietario1'],
                cpf_proprietario2 = form.cleaned_data['cpf_proprietario2'],
                cpf_testemunha1 = form.cleaned_data['cpf_testemunha1'],
                cpf_testemunha2 = form.cleaned_data['cpf_testemunha2']
            )
            formulario.save()
            
            context = {
                'centrocustos': centrocustos,
                'form' : form,
                'filtros': filtros,
                'usuario': usuario,
            }

            messages.success(
                request, 'A tarefa foi cadastrada com sucesso!', extra_tags='success')
            # return HttpResponseRedirect(reverse('Tarefa:editar', args=(tarefa.id_tarefa,)))
            return render(request, 'entregachaves.html', context)
        else:
            context = {
                'centrocustos': centrocustos,
                'form' : form,
                'filtros': filtros,
                'usuario': usuario,
            }
            messages.success(
                request, 'Falha ao cadastrar o formulário!', extra_tags='danger')
            return render(request, 'entregachaves.html', context)

    context = {
        'centrocustos': centrocustos,
        'form' : form,
        'filtros': filtros,
        'usuario': usuario,
    }
    return render(request, 'entregachaves.html', context)