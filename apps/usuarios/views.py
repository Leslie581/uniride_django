from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

# Para seguridad de contraseñas
from django.contrib.auth.hashers import make_password, check_password

from .models import Usuario, Cuenta

# ==========================
# HOME (pantalla inicial)
# ==========================
def home(request):
    return render(request, 'usuarios/home.html')

# ==========================
# REGISTRO
# ==========================
def registro(request):
    if request.method == 'POST':

        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        telefono = request.POST.get('telefono')

        username = request.POST.get('username')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        confirmar = request.POST.get('confirmar')

        es_pasajero = request.POST.get('es_pasajero') == 'on'
        es_conductor = request.POST.get('es_conductor') == 'on'

        foto = request.FILES.get('foto_perfil')
        terminos = request.POST.get('terminos')

        # ================= VALIDACIONES =================
        # Campos obligatorios
        if not all([nombre, apellidos, fecha_nacimiento, telefono, username, correo, contrasena, confirmar]):
            messages.error(request, 'Todos los campos son obligatorios')
            return redirect('registro')

        # Foto obligatoria
        if not foto:
            messages.error(request, 'Debes subir una foto de perfil')
            return redirect('registro')

        # Aceptar términos obligatorio
        if not terminos:
            messages.error(request, 'Debes aceptar los términos')
            return redirect('registro')

        # Contraseñas iguales
        if contrasena != confirmar:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('registro')

        # Usuario único
        if Cuenta.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return redirect('registro')

        # Correo único
        if Cuenta.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo ya está registrado')
            return redirect('registro')

        # Al menos un rol
        if not es_pasajero and not es_conductor:
            messages.error(request, 'Selecciona al menos un rol')
            return redirect('registro')

        # ================= CREACIÓN =================
        usuario = Usuario.objects.create(
            nombre=nombre,
            apellidos=apellidos,
            fecha_nacimiento=fecha_nacimiento,
            telefono=telefono,
            foto_perfil=foto,
            es_pasajero=es_pasajero,
            es_conductor=es_conductor,
            activo=True
        )

        # Guardar contraseña en HASH
        Cuenta.objects.create(
            usuario=usuario,
            username=username,
            correo=correo,
            contrasena=make_password(contrasena),
            activo=True
        )

        messages.success(request, 'Registro exitoso')
        return redirect('login')

    return render(request, 'usuarios/registro.html')

# ==========================
# LOGIN
# ==========================
def login_view(request):
    if request.method == 'POST':
        usuario_input = request.POST.get('usuario')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        try:
            cuenta = Cuenta.objects.get(
                Q(username=usuario_input) | Q(correo=usuario_input)
            )
        except Cuenta.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            return redirect('login')

        # Validar contraseña (hash)
        if not check_password(password, cuenta.contrasena):
            messages.error(request, 'Contraseña incorrecta')
            return redirect('login')

        usuario = cuenta.usuario

        # Validar rol
        if rol == 'pasajero' and not usuario.es_pasajero:
            messages.error(request, 'No tienes rol de pasajero')
            return redirect('login')

        if rol == 'conductor' and not usuario.es_conductor:
            messages.error(request, 'No tienes rol de conductor')
            return redirect('login')

        # Guardar sesión
        request.session['usuario_id'] = usuario.id
        request.session['rol_activo'] = rol

        # Redirigir según rol
        if rol == 'pasajero':
            return redirect('inicio_pasajero')
        else:
            return redirect('inicio_conductor')

    return render(request, 'usuarios/login.html')

# ==========================
# LOGOUT
# ==========================
def logout_view(request):
    request.session.flush()
    return redirect('login')

# ==========================
# REDIRECCIÓN GENERAL
# ==========================
def inicio(request):
    rol = request.session.get('rol_activo')

    if not rol:
        return redirect('login')

    if rol == 'pasajero':
        return redirect('inicio_pasajero')
    else:
        return redirect('inicio_conductor')

# ==========================
# INICIO PASAJERO
# ==========================
def inicio_pasajero(request):
    usuario_id = request.session.get('usuario_id')
    rol = request.session.get('rol_activo')

    if not usuario_id or rol != 'pasajero':
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    return render(request, 'usuarios/inicio_pasajero.html', {
        'usuario': usuario,
        'rol': 'Pasajero'
    })

# ==========================
# INICIO CONDUCTOR
# ==========================
def inicio_conductor(request):
    usuario_id = request.session.get('usuario_id')
    rol = request.session.get('rol_activo')

    if not usuario_id or rol != 'conductor':
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    return render(request, 'usuarios/inicio_conductor.html', {
        'usuario': usuario,
        'rol': 'Conductor'
    })

# ==========================
# PERFIL
# ==========================
def perfil(request):
    usuario_id = request.session.get('usuario_id')


    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)

    return render(request, 'usuarios/perfil.html', {
        'usuario': usuario
    })

# ==========================
# CAMBIAR ROL
# ==========================
def cambiar_rol(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)
    nuevo_rol = request.POST.get('rol')

    if nuevo_rol == 'pasajero' and usuario.es_pasajero:
        request.session['rol_activo'] = 'pasajero'


    elif nuevo_rol == 'conductor' and usuario.es_conductor:
        request.session['rol_activo'] = 'conductor'

    return redirect('inicio')
