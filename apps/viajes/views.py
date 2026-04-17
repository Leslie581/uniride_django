from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Vehiculo, Ruta, Viaje, Solicitud
from apps.usuarios.models import Usuario


# =====================================
# CREAR VEHÍCULO (CONDUCTOR)
# =====================================
def crear_vehiculo(request):
    usuario_id = request.session.get('usuario_id')
    rol = request.session.get('rol_activo')

    if not usuario_id or rol != 'conductor':
        return redirect('login')

    if request.method == 'POST':
        Vehiculo.objects.create(
            conductor_id=usuario_id,
            marca=request.POST['marca'],
            modelo=request.POST['modelo'],
            anio=request.POST['anio'],
            placas=request.POST['placas'],
            color=request.POST['color'],
            activo=True
        )
        messages.success(request, "Vehículo creado")
        return redirect('lista_vehiculos')

    return render(request, 'viajes/crear_vehiculo.html')


# =====================================
# LISTAR VEHÍCULOS
# =====================================
def lista_vehiculos(request):
    usuario_id = request.session.get('usuario_id')

    vehiculos = Vehiculo.objects.filter(conductor_id=usuario_id)

    return render(request, 'viajes/lista_vehiculos.html', {
        'vehiculos': vehiculos
    })


# =====================================
# CREAR RUTA
# =====================================
def crear_ruta(request):
    usuario_id = request.session.get('usuario_id')

    if request.method == 'POST':
        Ruta.objects.create(
            conductor_id=usuario_id,
            origen=request.POST['origen'],
            destino=request.POST['destino']
        )
        return redirect('lista_rutas')

    return render(request, 'viajes/crear_ruta.html')


# =====================================
# LISTAR RUTAS
# =====================================
def lista_rutas(request):
    usuario_id = request.session.get('usuario_id')

    rutas = Ruta.objects.filter(conductor_id=usuario_id)

    return render(request, 'viajes/lista_rutas.html', {
        'rutas': rutas
    })


# =====================================
# CREAR VIAJE (NÚCLEO)
# =====================================
def crear_viaje(request):
    usuario_id = request.session.get('usuario_id')

    vehiculos = Vehiculo.objects.filter(conductor_id=usuario_id)
    rutas = Ruta.objects.filter(conductor_id=usuario_id)

    if request.method == 'POST':
        Viaje.objects.create(
            conductor_id=usuario_id,
            vehiculo_id=request.POST['vehiculo'],
            ruta_id=request.POST['ruta'],
            fecha=request.POST['fecha'],
            hora=request.POST['hora'],
            asientos_disponibles=request.POST['asientos'],
            precio=request.POST['precio'],
        )
        return redirect('mis_viajes')

    return render(request, 'viajes/crear_viaje.html', {
        'vehiculos': vehiculos,
        'rutas': rutas
    })


# =====================================
# MIS VIAJES (CONDUCTOR)
# =====================================
def mis_viajes(request):
    usuario_id = request.session.get('usuario_id')

    viajes = Viaje.objects.filter(conductor_id=usuario_id)

    return render(request, 'viajes/mis_viajes.html', {
        'viajes': viajes
    })


# =====================================
# LISTA VIAJES (PASAJERO)
# =====================================
def listar_viajes(request):
    viajes = Viaje.objects.filter(activo=True)

    return render(request, 'viajes/listar_viajes.html', {
        'viajes': viajes
    })


# =====================================
# SOLICITAR VIAJE
# =====================================
def solicitar_viaje(request, viaje_id):
    usuario_id = request.session.get('usuario_id')

    viaje = get_object_or_404(Viaje, id=viaje_id)

    Solicitud.objects.create(
        viaje=viaje,
        pasajero_id=usuario_id
    )

    messages.success(request, "Solicitud enviada")
    return redirect('listar_viajes')