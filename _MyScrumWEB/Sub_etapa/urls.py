from django.urls import path

from . import views

app_name = 'Sub_etapa'

urlpatterns = [
    path('cadastrar/', views.cadastrarSub_etapa, name='cadastrarSub_etapa'),
    path('editar/', views.editarSub_etapa, name='editarSub_etapa'),
]
