from django.db import models
from django.core.exceptions import ValidationError
from django.db import models

from clientes.models import Cliente
from habitaciones.models import Habitacion


class Reservacion(models.Model):
    ACTIVA = 'activa'
    CANCELADA = 'cancelada'
    FINALIZADA = 'finalizada'

    ESTADOS = [
        (ACTIVA, 'Activa'),
        (CANCELADA, 'Cancelada'),
        (FINALIZADA, 'Finalizada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT,
                                related_name='reservaciones')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.PROTECT,
                                   related_name='reservaciones')
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2,
                                default=0, editable=False)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ACTIVA)

    class Meta:
        ordering = ['-fecha_entrada']
        verbose_name = 'Reservación'
        verbose_name_plural = 'Reservaciones'

    def __str__(self):
        return f"Reservación #{self.pk} - {self.cliente} - Hab. {self.habitacion.numero}"

    @property
    def noches(self):
        return (self.fecha_salida - self.fecha_entrada).days

    def clean(self):
        super().clean()

        # Si faltan fechas, los errores de campo ya los reporta el formulario
        if not (self.fecha_entrada and self.fecha_salida):
            return

        # Regla 2
        if self.fecha_salida <= self.fecha_entrada:
            raise ValidationError(
                {'fecha_salida': 'La fecha de salida debe ser mayor que la fecha de entrada.'}
            )

        if self.habitacion_id and self.estado == self.ACTIVA:
            # Regla 1: solo cuentan las reservaciones activas de ESTA habitación
            choques = Reservacion.objects.filter(
                habitacion_id=self.habitacion_id,
                estado=self.ACTIVA,
                fecha_entrada__lt=self.fecha_salida,
                fecha_salida__gt=self.fecha_entrada,
            ).exclude(pk=self.pk)

            if choques.exists():
                raise ValidationError(
                    'La habitación ya está reservada en esas fechas.'
                )

    def save(self, *args, **kwargs):
        self.total = self.noches * self.habitacion.precioxnoche
        super().save(*args, **kwargs)
# Create your models here.
