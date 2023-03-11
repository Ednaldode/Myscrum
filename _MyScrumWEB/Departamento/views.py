#Import Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

#Import do mesmo App
from .forms import DepartamentoForms
from .models import Departamento

# Create your views here.
def editarDepartamento(request):
    #dptos = get_object_or_404(Departamento, pk=id)
    #form = DepartamentoForms(request.POST or None, instance=dptos)

    context = {
        #"dptos": dptos,
        #"form": form,
    }
    return render(request, "editarDepartamento.html", context)

def cadastrarDepartamento(request):
    form_departamento = DepartamentoForms()
    departamentos = Departamento.objects.all()

    if request.method == 'POST':
        print(request.POST)
        try:
            departamento = request.POST['departamento']

            dpto = Departamento(departamento=departamento)
            dpto.save()
            messages.success(request, 'Departamento cadastrado com sucesso', extra_tags='success')
        except:
            messages.error(request, 'Não foi possível cadastrar o Departamento. Tente novamente!', extra_tags='danger')

    context = {
        "form_departamento": form_departamento,
        "departamentos": departamentos,
    }
    return render(request, 'cadastroDepartamento.html', context)