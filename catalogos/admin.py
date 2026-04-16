from django.contrib import admin
from .models import Estado

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_estado', 'tipo_entidad')
    list_filter = ('tipo_entidad',)
    search_fields = ('nombre_estado',)
    ordering = ('tipo_entidad', 'nombre_estado')