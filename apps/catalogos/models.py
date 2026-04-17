from django.db import models

class Estado(models.Model):

    # TIPOS DE ENTIDAD (SOLO LOS QUE USARÁS)
    TIPO_ENTIDAD_CHOICES = [
        ('viaje', 'Viaje'),
        ('solicitud', 'Solicitud'),
    ]

    # ESTADOS CONTROLADOS
    ESTADOS_VIAJE = [
        ('disponible', 'Disponible'),
        ('lleno', 'Lleno'),
        ('cancelado', 'Cancelado'),
        ('finalizado', 'Finalizado'),
    ]

    ESTADOS_SOLICITUD = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada'),
    ]

    nombre_estado = models.CharField(max_length=20)
    tipo_entidad = models.CharField(max_length=20, choices=TIPO_ENTIDAD_CHOICES)

    class Meta:
        db_table = 'Estado'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        unique_together = ('nombre_estado', 'tipo_entidad')
        ordering = ['tipo_entidad', 'nombre_estado']

    def __str__(self):
        return f"{self.nombre_estado} - {self.tipo_entidad}"