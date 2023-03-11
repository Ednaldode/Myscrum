from django.urls import path

from . import views
# from Tarefa.views import getProblemas

app_name = 'Fluxo'

urlpatterns = [
    path('fluxo', views.fluxo, name='fluxo'),
    path('juridico', views.juridico, name='juridico'),
    path('solicitacao', views.solicitacao, name='solicitacao'),
    path('conservacao', views.conservacao, name='conservacao'),
    path('locacao', views.locacao, name='locacao'),
    path('exportar/locacao', views.exportarLocacao, name='exportarLocacao'),
    path('exportar/conservacao', views.exportarConservacao, name='exportarConservacao'),
    path('exportar/medicao/terceiros', views.exportarMedicao, name='exportarMedicao'),
    path('medicao/terceiros', views.medicaoTerceiros, name='medicaoTerceiros'),
    path('editar/locacao/<int:id>', views.editarLocacao, name='editarLocacao'),
]
    