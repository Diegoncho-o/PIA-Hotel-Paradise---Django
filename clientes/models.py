from django.db import models



class Cliente(models.Model):

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    def save(self, *args, **kwargs):
        self.correo = self.correo.strip().lower()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['apellidos', 'nombre']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


# Create your models here.
