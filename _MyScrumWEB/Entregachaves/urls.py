from unicodedata import name
from django.urls import path

from . import views

app_name = 'Entregachaves'

urlpatterns = [
    path('Entregachaves', views.entregachaves, name='entregachaves'),
]
