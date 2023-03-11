from django.shortcuts import render

# Create your views here.

def cadastarEtapa(request):
    return render(request, 'cadastrarEtapa.html')

def editarEtapa(request):
    return render(request, 'editarEtapa.html')