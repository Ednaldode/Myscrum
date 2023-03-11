from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'Espelho'

urlpatterns = [
    path('', views.espelho, name='espelhovendas'),
    path('vistoria', views.vistoria, name='espelhovistorias'),
    path('pendencias', views.pendencias, name="pendenciasvistoria"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
