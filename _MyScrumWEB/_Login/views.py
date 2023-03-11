# Import Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

# Import de outros Apps
from Centro_de_custo.models import CentroCusto
from Departamento.models import Departamento
from _MyScrumWEB import urls

# Import de mesmo App
from .backend import MyBackend
from .forms import PessoaForms, profileForm
from .models import Pessoa, Vinculos, ListarPessoas

# Import Biblioteca python
from datetime import date, datetime
import json

# Create your views here.

def get_user(id_user):
    usuario = Pessoa.objects.get(id_user=id_user)
    tempo_empresa = date.today() - usuario.data_contratacao
    days = tempo_empresa.days
    years, days = days // 365, days % 365
    months, days = days // 30, days % 30

    if years ==1:
        usuario.data_contratacao = ''' {} ano, {} meses e {} dias.'''.format(years, months, days)
        if years == 1 and months == 1:
            usuario.data_contratacao = ''' {} ano, {} mês e {} dias.'''.format(years, months, days)
        if years == 1 and months == 1 and days == 1:
            usuario.data_contratacao = ''' {} ano, {} mês e {} dia.'''.format(years, months, days)

    elif years == 0:
        usuario.data_contratacao = '''{} meses e {} dias.'''.format(months, days)
        if months == 0:
            usuario.data_contratacao = '''{} dias.'''.format(days)
        if days == 1:
            usuario.data_contratacao = '''{} dia.'''.format(days)
        if months == 1:
            usuario.data_contratacao = ''' {}mês e {} dias.'''.format(months, days)
    else:
        usuario.data_contratacao = '''{} anos, {} meses e {} dias.'''.format(years, months, days)

    return usuario

def do_login(request):
    if request.method == 'POST':
        if MyBackend.checkUser(username=request.POST['username']) == False:
            messages.warning(request, 'Usuario não existente', extra_tags='warning')
            # Evento back usuario incorreto
        else:
            if MyBackend.checkPassword(username=request.POST['username'], password=request.POST['password']) == False:
                messages.warning(request, 'Senha incorreta', extra_tags='danger')
                # Evento back senha incorreta
        user = MyBackend.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect(f'''{urls.subdominio}/home''')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def do_logout(request):
    logout(request)
    return redirect(f'''/{urls.subdominio}/sessao/login''')

@login_required(login_url=urls.getUrlSubdominio())
def usuarios(request):
    usuario = get_user(request.user)

    if usuario.adm == 1:

        form_user = UserCreationForm()
        form_pessoa = PessoaForms()
        pessoas = ListarPessoas.objects.all()
        centrosDecusto = CentroCusto.objects.all()
        departamentos = Departamento.objects.all()

        context = {
            "form_user" : form_user,
            "form_pessoa" : form_pessoa,
            "usuario" : usuario,
            "pessoas": pessoas,
            "centrosDecusto" : centrosDecusto,
            "departamentos" : departamentos
        }

        return render(request, 'usuarios.html', context)
    else:
        messages.success(request, 'Área restrita para administradores', extra_tags='warning')
        return redirect(f'''{urls.subdominio}/home''')


def cadastrarUsuarios(request):
    if request.method == 'POST':
        form_user = UserCreationForm(request.POST)
        form_pessoa = PessoaForms(request.POST)

        if form_user.is_valid():
            form_user.save()
            try:
                nome = request.POST['nome']
                usuario = request.POST['username']
                email = request.POST['email']
                senha = request.POST['password1']
                funcao = request.POST['funcao']
                ativo = request.POST['ativo']
                salario = request.POST['salario']
                carga_horaria = request.POST['carga_horaria']
                observacao = request.POST['observacao']
                data_contratacao = datetime.strptime(request.POST['data_contratacao'], "%d/%m/%Y")
                departamento = Departamento.objects.get(pk=request.POST['id_departamento'])
                centrocusto = CentroCusto.objects.get(pk=request.POST['id_centrocusto'])
                id_user = User.objects.get(username=usuario)

                pessoa = Pessoa(nome=nome, login=usuario, email=email, senha=senha, 
                adm=int(funcao), ativo=int(ativo), salario=salario, carga_horaria=carga_horaria,
                observacao=observacao, data_contratacao=data_contratacao,
                id_departamento=departamento, id_centrocusto=centrocusto,
                id_user=id_user)

                pessoa.save()
                messages.success(request, 'Usuario cadastrado com sucesso', extra_tags='success')

                form_pessoa = PessoaForms()
                form_user = UserCreationForm()

            except:
                messages.error(request, 'Não foi possível cadastrar o usuario. Tente novamente!', extra_tags='danger')
                return redirect('_Login:usuarios')
        else:
            for erro, msg in form_user.errors.items():
                messages.error(request, msg, extra_tags='danger')

            return redirect('_Login:usuarios')

    return redirect('_Login:usuarios')

def editarUsuarios(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        instance_user = Pessoa.objects.get(pk=request.POST['id_pessoa'])
        user = User.objects.get(pk=instance_user.id_user.pk)

        # Verificamos se os campos de senhas são diferente de vazios para definirmo se a senha vai ser atualizada
        if password1 != '' and password2 != '':
            if password1 == password2:
                if user != request.user:
                    user.set_password(password1)
                    user.save()
                    updateUser(request)

                else:
                    messages.error(request, 'Favor usar a pagina de alteração de senha para alterar sua propria senha', extra_tags='danger')
                    return redirect('_Login:usuarios')
            else:
                messages.error(request, 'As senhas não são iguais', extra_tags='danger')
                return redirect('_Login:usuarios')
        else:
            # Se os campos de senha forem vazio chamamos o updateUser()
            updateUser(request)

    return redirect('_Login:usuarios')

def editarUser(request, id):
    if request.method == 'GET' and request.is_ajax():
        user = Pessoa.objects.filter(id_pessoa=id)

    data = serializers.serialize('json', list(user))

    return HttpResponse(json.dumps(data))

def getVinculosCC(request, id):
    if request.method == 'GET' and request.is_ajax():
        vinculosCC = Vinculos.objects.filter(id_usuario=id, id_cc__isnull=False)

    data = serializers.serialize('json', list(vinculosCC))

    return HttpResponse(json.dumps(data))

def getVinculosDPTO(request, id):
    if request.method == 'GET' and request.is_ajax():
        vinculosDPTO = Vinculos.objects.filter(id_usuario=id, id_dpto__isnull=False)

    data = serializers.serialize('json', list(vinculosDPTO))

    return HttpResponse(json.dumps(data))

def updateUser(request):
    instance_user = Pessoa.objects.get(pk=request.POST['id_pessoa'])
    user = User.objects.get(pk=instance_user.id_user.pk)
    
    usuarios = User.objects.filter(username=request.POST['username']).exclude(pk=user.id)
    if len(usuarios) == 0:
        try:
            user.username = request.POST['username']

            user.save()

            pessoa = Pessoa.objects.get(pk=request.POST['id_pessoa'])

            pessoa.nome = request.POST['nome']
            pessoa.login = request.POST['username']
            pessoa.email = request.POST['email']
            pessoa.adm = request.POST['funcao']
            pessoa.ativo = request.POST['ativo']
            pessoa.salario = request.POST['salario']
            pessoa.carga_horaria = int(request.POST['carga_horaria'])
            pessoa.observacao = request.POST['observacao']
            pessoa.data_contratacao = datetime.strptime(request.POST['data_contratacao'], "%d/%m/%Y")
            pessoa.id_departamento = Departamento.objects.get(pk=request.POST['id_departamento'])
            pessoa.id_centrocusto = CentroCusto.objects.get(pk=request.POST['id_centrocusto'])

            pessoa.save()

            ################################### VINCULOS CENTRO DE CUSTO ######################################################
            vinculosCC_objects = Vinculos.objects.values_list('id_cc', flat=True).filter(id_usuario=pessoa, id_cc__isnull=False)
            vinculosCC = []

            for vinculo in vinculosCC_objects:
                vinculosCC.append(str(vinculo))
        

            # Adicionando os novos centro de custo aos vinculos
            for cc in request.POST.getlist('vinculosCC'):
                if cc not in vinculosCC:
                    vinculo = Vinculos(id_usuario=pessoa, id_cc=CentroCusto.objects.get(pk=cc))
                    vinculo.save()

            # Removendo os centrocustos deletados dos vinculos
            for vinculoCC in vinculosCC:
                if vinculoCC not in request.POST.getlist('vinculosCC'):
                    Vinculos.objects.filter(id_usuario=pessoa, id_cc=CentroCusto.objects.get(pk=vinculoCC)).delete()

            ################################### VINCULOS DEPARTAMENTO #######################################################
            vinculosDPTO_objects = Vinculos.objects.values_list('id_dpto', flat=True).filter(id_usuario=pessoa, id_dpto__isnull=False)
            vinculosDPTO = []

            for vinculo in vinculosDPTO_objects:
                vinculosDPTO.append(str(vinculo))
            
            # Adicionando os novos centro de custo aos vinculos
            for dpto in request.POST.getlist('vinculosDPTO'):
                if dpto not in vinculosDPTO:
                    vinculo = Vinculos(id_usuario=pessoa, id_dpto=Departamento.objects.get(pk=dpto))
                    vinculo.save()

            # Removendo os centrocustos deletados dos vinculos
            for vinculoDPTO in vinculosDPTO:
                if vinculoDPTO not in request.POST.getlist('vinculosDPTO'):
                    vinculo = Vinculos.objects.filter(id_usuario=pessoa, id_dpto=Departamento.objects.get(pk=vinculoDPTO)).delete()
                


            messages.success(request, 'Usuario atualizado com sucesso', extra_tags='success')

        except:
            messages.error(request, 'Não foi possível atualizar o usuario. Tente novamente!', extra_tags='danger')
    else:
        messages.success(request, 'Já existe um usuario com este login/username', extra_tags='success')


    return ''
