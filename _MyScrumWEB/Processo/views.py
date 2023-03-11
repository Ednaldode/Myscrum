from django.shortcuts import render

# Create your views here.

def cadastrarProcesso(request):
    return render(request, 'cadastrarProcesso.html')

def editarProcesso(request):
    return render(request, 'editarProcesso.html')