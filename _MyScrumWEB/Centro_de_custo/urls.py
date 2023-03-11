from django.urls import path

from . import views

app_name = 'Centro_de_custo'

urlpatterns = [
    path('cadastrar/', views.cadastrarCentro_de_custo, name='cadastrarCentro_de_custo'),
    path('editar/', views.editarCentro_de_custo, name='editarCentro_de_custo'),
]
