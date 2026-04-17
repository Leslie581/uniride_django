from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),

    # path('inicio/', views.inicio, name='inicio'),

    # path('inicio/pasajero/', views.inicio_pasajero, name='inicio_pasajero'),
    path('inicio/conductor/', views.inicio_conductor, name='inicio_conductor'),

    # path('perfil/', views.perfil, name='perfil'),
    # path('cambiar-rol/', views.cambiar_rol, name='cambiar_rol'),
]