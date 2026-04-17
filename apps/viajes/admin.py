from django.contrib import admin
from .models import Vehiculo, Ruta, PuntoIntermedio, Viaje, Solicitud


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'conductor', 'marca', 'modelo', 'placas', 'activo')


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('id', 'conductor', 'origen', 'destino')


@admin.register(PuntoIntermedio)
class PuntoIntermedioAdmin(admin.ModelAdmin):
    list_display = ('id', 'ruta', 'nombre', 'orden')
    ordering = ('ruta', 'orden')


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'conductor', 'ruta', 'fecha', 'hora', 'precio', 'activo')


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'viaje', 'pasajero', 'estado', 'fecha_solicitud')