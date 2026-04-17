from django.urls import path
from . import views

urlpatterns = [
    path('vehiculos/', views.lista_vehiculos, name='lista_vehiculos'),
    path('vehiculos/crear/', views.crear_vehiculo, name='crear_vehiculo'),

    path('rutas/', views.mis_rutas, name='mis_rutas'),
    path('rutas/crear/', views.crear_ruta, name='crear_ruta'),

    path('viajes/', views.listar_viajes, name='listar_viajes'),
    path('viajes/crear/', views.crear_viaje, name='crear_viaje'),
    path('viajes/mis/', views.mis_viajes, name='mis_viajes'),

    path('viaje/solicitar/<int:viaje_id>/', views.solicitar_viaje, name='solicitar_viaje'),
]