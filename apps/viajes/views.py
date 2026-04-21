from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime

from .models import Vehiculo, Ruta, Viaje, Solicitud,PuntoIntermedio
from apps.usuarios.models import Usuario
from apps.catalogos.models import Estado


# ==========================
# VALIDACIÓN DE SESIÓN
# ==========================
def validar_conductor(request):
    usuario_id = request.session.get('usuario_id')
    rol = request.session.get('rol_activo')

    if not usuario_id or rol != 'conductor':
        return None
    return usuario_id


def validar_pasajero(request):
    usuario_id = request.session.get('usuario_id')
    rol = request.session.get('rol_activo')

    if not usuario_id or rol != 'pasajero':
        return None
    return usuario_id


# ==========================
# VEHÍCULOS
# ==========================
def lista_vehiculos(request):
    usuario_id = validar_conductor(request)
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    vehiculos = Vehiculo.objects.filter(conductor_id=usuario_id)

    return render(request, 'viajes/lista_vehiculos.html', {
        'vehiculos': vehiculos,
        'usuario': usuario,
        'rol': 'Conductor'
    })


def crear_vehiculo(request):
    usuario_id = validar_conductor(request)
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        Vehiculo.objects.create(
            conductor_id=usuario_id,
            marca=request.POST['marca'],
            modelo=request.POST['modelo'],
            placas=request.POST['placas'],
            color=request.POST['color'],
            capacidad=request.POST['capacidad'],
            activo=True
        )

        messages.success(request, "Vehículo creado")
        return redirect('lista_vehiculos')

    return render(request, 'viajes/crear_vehiculo.html', {
        'usuario': usuario,
        'rol': 'Conductor'
    })


# ==========================
# RUTAS
# ==========================
def lista_rutas(request):
    usuario_id = validar_conductor(request)
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    rutas = Ruta.objects.filter(conductor_id=usuario_id)

    return render(request, 'viajes/lista_rutas.html', {
        'rutas': rutas,
        'usuario': usuario,
        'rol': 'Conductor'
    })


def crear_ruta(request):
    usuario_id = validar_conductor(request)
    if not usuario_id:
        return redirect('login')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        # 1. Creamos la Ruta principal
        nueva_ruta = Ruta.objects.create(
            conductor_id=usuario_id,
            nombre=request.POST.get('nombre'),
            origen=request.POST.get('origen'),
            destino=request.POST.get('destino'),
            activo=True
        )

        # 2. Obtenemos la lista de nombres de puntos intermedios    
        nombres_puntos = request.POST.getlist('puntos_nombres')

        # 3. Guardamos cada punto intermedio en la base de datos
        for indice, nombre_lugar in enumerate(nombres_puntos):
            if nombre_lugar.strip():  # Solo guardamos si no está vacío
                PuntoIntermedio.objects.create(
                    ruta=nueva_ruta,
                    nombre_lugar=nombre_lugar,
                    # Como aún no hay mapa real, ponemos coordenadas en 0.0
                    latitud=0.0,
                    longitud=0.0,
                    orden=indice + 1  # Para mantener el orden en que se agregaron
                )

        messages.success(request, "Ruta creada correctamente")
        return redirect('lista_rutas')

    return render(request, 'viajes/crear_ruta.html', {
        'usuario': usuario,
        'rol': 'Conductor'
    })


# ==========================
# VIAJES
# ==========================
def crear_viaje(request):
    usuario_id = validar_conductor(request)
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    vehiculos = Vehiculo.objects.filter(conductor_id=usuario_id, activo=True)
    rutas = Ruta.objects.filter(conductor_id=usuario_id, activo=True)

    if request.method == 'POST':
        try:
            fecha = request.POST['fecha']
            hora = request.POST['hora']

            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")

            estado = Estado.objects.get(
                nombre_estado='disponible',
                tipo_entidad='viaje'
            )

            Viaje.objects.create(
                vehiculo_id=request.POST['vehiculo'],
                ruta_id=request.POST['ruta'],
                fecha_horario_viaje=fecha_hora,
                asientos_disponibles=request.POST['asientos'],
                precio=request.POST['precio'],
                estado=estado
            )

            messages.success(request, "Viaje publicado")
            return redirect('mis_viajes')

        except Exception as e:
            messages.error(request, f"Error al crear viaje: {str(e)}")

    return render(request, 'viajes/crear_viaje.html', {
        'vehiculos': vehiculos,
        'rutas': rutas,
        'usuario': usuario,
        'rol': 'Conductor'
    })


def mis_viajes(request):
    usuario_id = validar_conductor(request)
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    viajes = Viaje.objects.filter(
        vehiculo__conductor_id=usuario_id
    ).order_by('-fecha_horario_viaje')

    return render(request, 'viajes/mis_viajes.html', {
        'viajes': viajes,
        'usuario': usuario,
        'rol': 'Conductor'
    })


# ==========================
# PASAJERO - VER VIAJES
# ==========================
def listar_viajes(request):
    usuario_id = validar_pasajero(request)
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    estado = Estado.objects.get(
        nombre_estado='disponible',
        tipo_entidad='viaje'
    )

    viajes = Viaje.objects.filter(estado=estado)

    return render(request, 'viajes/listar_viajes.html', {
        'viajes': viajes,
        'usuario': usuario,
        'rol': 'Pasajero'
    })


# ==========================
# SOLICITAR VIAJE
# ==========================
def solicitar_viaje(request, viaje_id):
    usuario_id = validar_pasajero(request)
    if not usuario_id:
        return redirect('login')

    viaje = get_object_or_404(Viaje, id=viaje_id)

    estado = Estado.objects.get(
        nombre_estado='pendiente',
        tipo_entidad='solicitud'
    )

    Solicitud.objects.create(
        viaje=viaje,
        pasajero_id=usuario_id,
        estado=estado,
        punto_encuentro=request.POST.get('punto_encuentro', 'No definido')
    )

    messages.success(request, "Solicitud enviada")
    return redirect('listar_viajes')

# ==========================
# CAMBIAR ESTADO
# ==========================
def cambiar_estado_vehiculo(request, vehiculo_id):
    usuario_id = validar_conductor(request)
    if not usuario_id: return redirect('login')
    
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id, conductor_id=usuario_id)
    vehiculo.activo = not vehiculo.activo
    vehiculo.save()
    return redirect('lista_vehiculos')

def cambiar_estado_ruta(request, ruta_id):
    usuario_id = validar_conductor(request)
    if not usuario_id: return redirect('login')
    
    ruta = get_object_or_404(Ruta, id=ruta_id, conductor_id=usuario_id)
    ruta.activo = not ruta.activo
    ruta.save()
    return redirect('lista_rutas')