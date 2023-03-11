"""_MyScrumWEB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Para desenvolvimento deixar subdominio vazio
subdominio = ""
def getUrlSubdominio():
    if subdominio == "":
        return "/sessao/login"
    else:
        return f'''/{subdominio}/sessao/login'''

urlpatterns = [
    path('admin/''', admin.site.urls),
    path('sessao/''', include('_Login.urls')),
    path('home/''', include('Home.urls')),
    path('dashboards/''', include('Dashboards.urls')),
    path('', include('Home.urls')),
    path('tarefas/''', include('Tarefa.urls')),
    path('kanban/''', include('Kanban.urls')),
    path('espelho/''', include('Espelho.urls')),
    path('calendario/''', include('Calendario.urls')),
    path('retrospectiva/''', include('Retrospectiva.urls')),
    path('departamentos/', include('Departamento.urls')),
    path('solicitacao/', include('Solicitacao.urls')),
    path('fluxo/''', include('Fluxo.urls')),
    path ('entregachaves/''', include('Entregachaves.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
