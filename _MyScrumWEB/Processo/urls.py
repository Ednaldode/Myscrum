from django.urls import path

from . import views

app_name = 'Processo'

urlpatterns = [
    path('cadastrar/', views.cadastrarProcesso, name='cadastrarProcesso'),
    path('editar/', views.editarProcesso, name='editarProcesso'),
]
