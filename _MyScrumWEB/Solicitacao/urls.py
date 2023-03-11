from django.urls import path

from . import views
# from Tarefa.views import getProblemas

app_name = 'Solicitacao'

urlpatterns = [
    path('solicitacao', views.solicitacao, name='solicitacao'),
    path('cliente/', views.solicitacaoCliente, name='cliente'),
    path('impressao/<int:id>', views.impressao, name='impressao'),
    path('listar/', views.listar, name='listarSolicitacoes'),
    path('exportar/', views.exportarSolicitacoes, name='exportarSolicitacoes'),
    path('dashboardsSat/', views.dashboardsSat, name='dashboards'),

    # URLs Ajax, duplicadas para uso da url reversa pelo JS
    path('getProblemas/<int:id>', views.getProblemas),
    path('getProblemas/', views.getProblemas, name='getProblemas'),
]
    