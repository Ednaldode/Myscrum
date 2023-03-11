from django.shortcuts import render

# Create your views here.

def cadastraSub_etapa(request):
    return render(request, 'cadastrarSub_etapa.html')

def editarSub_etapa(request):
    return render(request, 'editarSub_etapa')