from django.db import models
from apps.usuarios.models import Usuario


# =====================================
# VEHÍCULO
# =====================================
class Vehiculo(models.Model):
    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()

    placas = models.CharField(max_length=20)
    color = models.CharField(max_length=30)

    activo = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.marca} {self.modelo} - {self.placas}"


# =====================================
# RUTA
# =====================================
class Ruta(models.Model):
    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    origen = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)

    def _str_(self):
        return f"{self.origen} → {self.destino}"


# =====================================
# PUNTOS INTERMEDIOS
# =====================================
class PuntoIntermedio(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=255)
    orden = models.IntegerField()

    def _str_(self):
        return f"{self.nombre} ({self.orden})"

    class Meta:
        ordering = ['orden']


# =====================================
# VIAJE (EL CORE)
# =====================================
class Viaje(models.Model):
    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)

    fecha = models.DateField()
    hora = models.TimeField()

    asientos_disponibles = models.IntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    descripcion = models.TextField(blank=True, null=True)

    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.ruta} - {self.fecha}"


# =====================================
# SOLICITUD (RESERVAS)
# =====================================
class Solicitud(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    pasajero = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('aceptada', 'Aceptada'),
            ('rechazada', 'Rechazada'),
        ],
        default='pendiente'
    )

    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.pasajero} - {self.estado}"

    class Meta:
        unique_together = ('viaje', 'pasajero')