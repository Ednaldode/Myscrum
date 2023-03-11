from django.contrib import admin
from .models import Pessoa


# Register your models here.
# admin.site.register(Pessoa)

@admin.register(Pessoa)
class Pessoa(admin.ModelAdmin):
    list_display = ['nome','login']
