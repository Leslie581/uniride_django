from django.db import models
from datetime import date

# ==========================
# USUARIO
# ==========================
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateField(auto_now_add=True)

    # Imagen de perfil (YA con Pillow)
    foto_perfil = models.ImageField(
        upload_to='perfiles/',
        null=False,
        blank=False
    )

    # Roles
    es_pasajero = models.BooleanField(default=True)
    es_conductor = models.BooleanField(default=False)

    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Usuario'

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    # Edad automática
    @property
    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )


# ==========================
# CUENTA (LOGIN)
# ==========================
class Cuenta(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    username = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)

    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Cuenta'

    def __str__(self):
        return self.username