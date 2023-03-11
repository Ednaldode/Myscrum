from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'Kanban'

urlpatterns = [
    path('', views.kanban, name='kanban'),
    path('exibir/tarefa/<int:id>', views.exibirTarefa, name='exibirTarefaKanban'),
    path('editar/tarefa', views.editarTarefa, name='editarTarefaKanban'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
