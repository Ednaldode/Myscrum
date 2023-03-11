from django.urls import path, include

from . import views

app_name = '_Login'

urlpatterns = [
    path('login/', views.do_login, name='do_login'),
    path('logout/', views.do_logout, name='do_logout'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/cadastrar', views.cadastrarUsuarios, name='cadastrarUsuarios'),
    path('usuarios/editar', views.editarUsuarios, name='editarUsuarios'),
    path('editarUser/<int:id>/', views.editarUser, name='editarUser'),
    path('getVinculosCC/<int:id>/', views.getVinculosCC, name='getVinculosCC'),
    path('getVinculosDPTO/<int:id>/', views.getVinculosDPTO, name='getVinculosDPTO'),
    path('', include('Home.urls')),
]
