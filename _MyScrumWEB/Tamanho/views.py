from django.shortcuts import render

# Create your views here.

def cadastrarTamanho(request):
    return render(request, 'cadastrarTamanho.html')

def editarTamanho(request):
    return render(request, 'editarTamanho')