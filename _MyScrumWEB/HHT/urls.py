from django.urls import path

from . import views

app_name = 'HHT'

urlpatterns = [
    path('', views.hht, name='hht'),
]
