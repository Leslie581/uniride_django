from django.db import models

from datetime import date
from django.core.validators import FileExtensionValidator

# ==========================
# USUARIO
# ==========================
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateField(auto_now_add=True)

    # Archivos (SIN Pillow)
    foto_perfil = models.FileField(
        upload_to='perfiles/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])]
    )

    identificacion = models.FileField(
        upload_to='identificaciones/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'pdf'])]
    )

    licencia = models.FileField(
        upload_to='licencias/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'pdf'])]
    )

    # Roles
    es_pasajero = models.BooleanField(default=True)
    es_conductor = models.BooleanField(default=False)

    # Verificaciones
    verificado_identidad = models.BooleanField(default=False)
    verificado_conductor = models.BooleanField(default=False)

    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    # Edad calculada automáticamente
    @property
    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    # Lógica automática de verificación (clave para tu sistema)
    def save(self, *args, **kwargs):
        if self.identificacion:
            self.verificado_identidad = True

        if self.licencia:
            self.verificado_conductor = True

        super().save(*args, **kwargs)


# ==========================
# CUENTA (LOGIN)
# ==========================
class Cuenta(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='cuenta'
    )

    username = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)

    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Cuenta'
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'

    def __str__(self):
        return self.username