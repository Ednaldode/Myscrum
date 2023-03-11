from django.urls import path

from . import views

app_name = 'Etapa'

urlpatterns = [
    path('cadastrar/', views.cadastrarEtapa, name='cadastrarEtapa'),
    path('editar/', views.editarEtapa, name='editarEtapa'),
]
