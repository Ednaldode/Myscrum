from django.urls import path

from . import views

app_name = 'Retrospectiva'

urlpatterns = [
    path('', views.retrospectiva, name='retrospectiva'),
    path('exportar/retrospectiva', views.exportarRetrospectivas, name='ExportarRetrospectiva'),
]
