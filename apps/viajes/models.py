from django.db import models
from apps.usuarios.models import Usuario
from apps.catalogos.models import Estado


# =====================================
# VEHÍCULO
# =====================================
class Vehiculo(models.Model):
    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    placas = models.CharField(max_length=20)
    capacidad = models.IntegerField()

    activo = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.marca} {self.modelo} - {self.placas}"


# =====================================
# RUTA
# =====================================
class Ruta(models.Model):
    conductor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=100)
    origen = models.CharField(max_length=50)
    destino = models.CharField(max_length=50)

    activo = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.nombre} ({self.origen} → {self.destino})"


# =====================================
# PUNTOS INTERMEDIOS
# =====================================
class PuntoIntermedio(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)

    nombre_lugar = models.CharField(max_length=150)
    latitud = models.DecimalField(max_digits=10, decimal_places=8)
    longitud = models.DecimalField(max_digits=11, decimal_places=8)

    orden = models.IntegerField()

    def _str_(self):
        return f"{self.nombre_lugar} ({self.orden})"

    class Meta:
        ordering = ['orden']


# =====================================
# VIAJE
# =====================================
class Viaje(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    fecha_horario_viaje = models.DateTimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    asientos_disponibles = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"{self.ruta} - {self.fecha_horario_viaje}"


# =====================================
# SOLICITUD
# =====================================
class Solicitud(models.Model):
    pasajero = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    punto_encuentro = models.CharField(max_length=150)

    def _str_(self):
        return f"{self.pasajero} - {self.estado}"

    class Meta:
        unique_together = ('pasajero', 'viaje')