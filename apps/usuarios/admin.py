from django.contrib import admin
from .models import Usuario, Cuenta


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'apellidos',
        'get_username',
        'telefono',
        'es_pasajero',
        'es_conductor',
        'verificado_identidad',
        'verificado_conductor'
    )

    search_fields = ('nombre', 'apellidos', 'telefono')
    list_filter = ('es_pasajero', 'es_conductor', 'verificado_identidad', 'verificado_conductor')

    def get_username(self, obj):
        return obj.cuenta.username if hasattr(obj, 'cuenta') else '-'
    get_username.short_description = 'Username'


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'correo', 'activo')
    search_fields = ('username', 'correo')