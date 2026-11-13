from django.db import models

# Create your models here.






class Habitacion(models.Model):

    TIPOS = [
        ('individual', 'Individual'),
        ('doble', 'Doble'),
        ('suite', 'Suite'),
        ('presidencial', 'Presidencial'),
    ]


    #llave primaria de la tabla
    numero = models.IntegerField(unique=True)
    #campo del tipo de la habitacion
    tipo =  models.CharField((""), max_length=20, choices=TIPOS)
    precioxnoche = models.DecimalField(max_digits=  15, decimal_places=2)
    capacidad = models.IntegerField()
    disponible = models.BooleanField(default= True)
    imagen = models.ImageField(upload_to='habitaciones/', blank=True, null=True)
    
    
    def __str__(self):
            return f"Habitación {self.numero} - {self.get_tipo_display()}"


class Meta:
    ordering = ['numero']
    verbose_name = 'Habitación'
    verbose_name_plural = 'Habitaciones'
