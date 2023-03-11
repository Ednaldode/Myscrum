from django.urls import path

from . import views

app_name = 'Dashboards'

urlpatterns = [
    path('analisar/', views.analisarDash, name='analisarDash'),
]
