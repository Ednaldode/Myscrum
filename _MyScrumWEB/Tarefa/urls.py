from django.urls import path, include
from . import views

app_name = 'Tarefa'

urlpatterns = [
    path('cadastrar/', views.cadastrarTarefas, name='cadastrar'),
    path('duplicar/<int:id>', views.duplicarTarefas, name='duplicar'),
    path('listar/', views.listarTarefas, name='listar'),
    path('importar/', views.importarTarefas, name='importarTarefas'),
    path('importar/solicitacao/', views.importarSolicitacao, name='importarSolicitacao'),
    path('exportar/', views.exportarTarefa, name='exportarTarefas'),
    path('exportar/mae-filho/', views.exportarMaeFilho, name='exportarMaeFilho'),
    path('importar/mae-filho/', views.importarMaeFilho, name='importarMaeFilho'),

    # URL Editar tarefa para uso do kanban no JS
    path('editar/', views.editarTarefas, name='URL_editarTarefa'),
    path('editar/<int:id>', views.editarTarefas, name='editar'),

    path('filhos/', views.cadastrarFilhos, name='filhos'),
    path('filhos/<int:id>', views.cadastrarFilhos, name='filhos'),

    # URLs Ajax, duplicadas para uso da url reversa pelo JS
    path('getEtapa/<int:id>', views.getEtapa),
    path('getEtapa/', views.getEtapa, name='getEtapa'),

    path('getSubEtapa/<int:id>', views.getSubEtapa),
    path('getSubEtapa/', views.getSubEtapa, name='getSubEtapa'),

    path('getRetrospectiva/<int:id>', views.getRetrospectiva),
    path('getRetrospectiva/', views.getRetrospectiva, name='getRetrospectiva'),

    path('getR5w2h/<int:id>', views.getR5w2h),
    path('getR5w2h/', views.getR5w2h, name='getR5w2h'),

    path('getProblemas/<int:id>', views.getProblemas),
    path('getProblemas/', views.getProblemas, name='getProblemas'),
]
