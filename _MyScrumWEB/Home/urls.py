from django.urls import path

from . import views

app_name = 'Home'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboards', views.dashboards, name='dashboards'),
    path('dashboardResult', views.dashboardResult, name='dashboardsResult'),
]
