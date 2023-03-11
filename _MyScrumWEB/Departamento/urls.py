from django.urls import path

from . import views

app_name = 'Departamento'

urlpatterns = [
    path('cadastrar/', views.cadastrarDepartamento, name='cadastrarDepartamento'),
    path('editar/', views.editarDepartamento, name='editarDepartamento'),
]
