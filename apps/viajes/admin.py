from django.contrib import admin
from .models import Vehiculo, Ruta, PuntoIntermedio, Viaje, Solicitud


# =====================================
# VEHÍCULO
# =====================================
@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marca', 'modelo', 'placas', 'capacidad', 'activo', 'conductor')
    search_fields = ('marca', 'modelo', 'placas')
    list_filter = ('activo', 'marca')
    list_editable = ('activo',)


# =====================================
# RUTA
# =====================================
class PuntoIntermedioInline(admin.TabularInline):
    model = PuntoIntermedio
    extra = 1


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'origen', 'destino', 'conductor', 'activo')
    search_fields = ('nombre', 'origen', 'destino')
    list_filter = ('conductor', 'activo')
    inlines = [PuntoIntermedioInline]


# =====================================
# PUNTO INTERMEDIO
# =====================================
@admin.register(PuntoIntermedio)
class PuntoIntermedioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_lugar', 'ruta', 'orden')
    search_fields = ('nombre_lugar',)
    list_filter = ('ruta',)


# =====================================
# VIAJE
# =====================================
@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):

    # 🔹 Método para mostrar conductor
    def get_conductor(self, obj):
        return obj.vehiculo.conductor
    get_conductor.short_description = 'Conductor'

    list_display = (
        'id',
        'get_conductor',
        'ruta',
        'vehiculo',
        'fecha_horario_viaje',
        'asientos_disponibles',
        'precio',
        'estado'
    )

    search_fields = (
        'vehiculo_conductor_nombre',
        'vehiculo_conductor_apellidos',
        'ruta__origen',
        'ruta__destino',
        'ruta__nombre',
        'vehiculo__placas'
    )

    list_filter = ('vehiculo__conductor', 'estado', 'fecha_horario_viaje')
    date_hierarchy = 'fecha_horario_viaje'


# =====================================
# SOLICITUD
# =====================================
@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pasajero',
        'viaje',
        'estado',
        'punto_encuentro',
        'fecha_solicitud'
    )

    search_fields = (
        'pasajero__nombre',
        'pasajero__apellidos',
        'viaje_ruta_nombre'
    )

    list_filter = ('estado',)