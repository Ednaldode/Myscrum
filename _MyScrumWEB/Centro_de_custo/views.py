from django.shortcuts import render

# Create your views here.

def cadastrarCentro_de_custo(request):
    return render(request, 'cadastrarCentro_de_custo.html')

def editarCentro_de_custo(request):
    return render(request, 'editarCentro_de_custo.html')