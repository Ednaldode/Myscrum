from django.urls import path

from . import views

app_name = 'Tamanho'

urlpatterns = [
    path('cadastar/', views.cadastrarTamanho, name='cadastrarTamanho'),
    path('editar/', views.editarTamanho, name='editarTamanho'),
]
